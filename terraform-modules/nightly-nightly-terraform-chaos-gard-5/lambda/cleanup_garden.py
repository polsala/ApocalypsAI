import json
import boto3
import os
import time

def lambda_handler(event, context):
    """
    Chaos Garden Cleanup Lambda Function
    
    This function performs cleanup of chaos garden resources
    to prevent resource sprawl and unexpected charges.
    """
    
    # Initialize AWS clients
    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')
    rds = boto3.client('rds')
    
    garden_name = os.environ.get('GARDEN_NAME', 'chaos-garden')
    
    cleanup_results = {
        'garden': garden_name,
        'timestamp': int(time.time()),
        'resources_cleaned': [],
        'errors': []
    }
    
    try:
        # Clean up EC2 instances
        cleanup_ec2_instances(ec2, garden_name, cleanup_results)
        
        # Clean up S3 buckets
        cleanup_s3_buckets(s3, garden_name, cleanup_results)
        
        # Clean up RDS instances
        cleanup_rds_instances(rds, garden_name, cleanup_results)
        
        # Clean up Lambda functions (log only, as they're managed by Terraform)
        cleanup_results['resources_cleaned'].append({
            'type': 'lambda_functions',
            'action': 'logged',
            'message': 'Lambda functions should be cleaned up by Terraform destroy'
        })
        
        return {
            'statusCode': 200,
            'body': json.dumps(cleanup_results, indent=2)
        }
        
    except Exception as e:
        cleanup_results['errors'].append({
            'error': str(e),
            'message': 'Cleanup failed'
        })
        
        return {
            'statusCode': 500,
            'body': json.dumps(cleanup_results, indent=2)
        }

def cleanup_ec2_instances(ec2, garden_name, cleanup_results):
    """Clean up EC2 instances in the chaos garden"""
    try:
        # Find instances with the garden tag
        response = ec2.describe_instances(
            Filters=[
                {'Name': 'tag:Garden', 'Values': [garden_name]},
                {'Name': 'tag:ChaosGarden', 'Values': ['true']}
            ]
        )
        
        instance_ids = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] in ['running', 'stopped']:
                    instance_ids.append(instance['InstanceId'])
        
        if instance_ids:
            # Terminate the instances
            ec2.terminate_instances(InstanceIds=instance_ids)
            
            cleanup_results['resources_cleaned'].append({
                'type': 'ec2_instances',
                'count': len(instance_ids),
                'instance_ids': instance_ids,
                'action': 'terminated',
                'message': f'Terminated {len(instance_ids)} EC2 instances'
            })
        else:
            cleanup_results['resources_cleaned'].append({
                'type': 'ec2_instances',
                'action': 'none_found',
                'message': 'No EC2 instances found to clean up'
            })
            
    except Exception as e:
        cleanup_results['errors'].append({
            'type': 'ec2_cleanup',
            'error': str(e),
            'message': 'Failed to clean up EC2 instances'
        })

def cleanup_s3_buckets(s3, garden_name, cleanup_results):
    """Clean up S3 buckets in the chaos garden"""
    try:
        # List all buckets
        response = s3.list_buckets()
        
        chaos_garden_buckets = [
            bucket['Name'] for bucket in response['Buckets']
            if garden_name in bucket['Name']
        ]
        
        cleaned_buckets = []
        for bucket_name in chaos_garden_buckets:
            try:
                # Delete all objects in the bucket
                objects = s3.list_objects_v2(Bucket=bucket_name)
                
                if 'Contents' in objects:
                    delete_keys = {'Objects': [{'Key': obj['Key']} for obj in objects['Contents']]}
                    s3.delete_objects(Bucket=bucket_name, Delete=delete_keys)
                
                # Delete the bucket
                s3.delete_bucket(Bucket=bucket_name)
                cleaned_buckets.append(bucket_name)
                
            except Exception as e:
                cleanup_results['errors'].append({
                    'type': 's3_bucket_cleanup',
                    'bucket': bucket_name,
                    'error': str(e),
                    'message': f'Failed to clean up bucket {bucket_name}'
                })
        
        if cleaned_buckets:
            cleanup_results['resources_cleaned'].append({
                'type': 's3_buckets',
                'count': len(cleaned_buckets),
                'bucket_names': cleaned_buckets,
                'action': 'deleted',
                'message': f'Deleted {len(cleaned_buckets)} S3 buckets'
            })
        else:
            cleanup_results['resources_cleaned'].append({
                'type': 's3_buckets',
                'action': 'none_found',
                'message': 'No S3 buckets found to clean up'
            })
            
    except Exception as e:
        cleanup_results['errors'].append({
            'type': 's3_cleanup',
            'error': str(e),
            'message': 'Failed to list S3 buckets'
        })

def cleanup_rds_instances(rds, garden_name, cleanup_results):
    """Clean up RDS instances in the chaos garden"""
    try:
        # Find RDS instances with the garden tag
        response = rds.describe_db_instances()
        
        instances_to_delete = []
        for db_instance in response['DBInstances']:
            # Check if this instance belongs to our garden
            tags_response = rds.list_tags_for_resource(ResourceName=db_instance['DBInstanceArn'])
            
            is_chaos_garden = False
            for tag in tags_response['TagList']:
                if tag['Key'] == 'Garden' and tag['Value'] == garden_name:
                    is_chaos_garden = True
                    break
                elif tag['Key'] == 'ChaosGarden' and tag['Value'] == 'true':
                    is_chaos_garden = True
                    break
            
            if is_chaos_garden and db_instance['DBInstanceStatus'] != 'deleting':
                instances_to_delete.append(db_instance['DBInstanceIdentifier'])
        
        deleted_instances = []
        for instance_id in instances_to_delete:
            try:
                # Delete the RDS instance
                rds.delete_db_instance(
                    DBInstanceIdentifier=instance_id,
                    SkipFinalSnapshot=True,
                    DeleteAutomatedBackups=True
                )
                deleted_instances.append(instance_id)
                
            except Exception as e:
                cleanup_results['errors'].append({
                    'type': 'rds_instance_cleanup',
                    'instance': instance_id,
                    'error': str(e),
                    'message': f'Failed to delete RDS instance {instance_id}'
                })
        
        if deleted_instances:
            cleanup_results['resources_cleaned'].append({
                'type': 'rds_instances',
                'count': len(deleted_instances),
                'instance_ids': deleted_instances,
                'action': 'deleted',
                'message': f'Deleted {len(deleted_instances)} RDS instances'
            })
        else:
            cleanup_results['resources_cleaned'].append({
                'type': 'rds_instances',
                'action': 'none_found',
                'message': 'No RDS instances found to clean up'
            })
            
    except Exception as e:
        cleanup_results['errors'].append({
            'type': 'rds_cleanup',
            'error': str(e),
            'message': 'Failed to list RDS instances'
        })
