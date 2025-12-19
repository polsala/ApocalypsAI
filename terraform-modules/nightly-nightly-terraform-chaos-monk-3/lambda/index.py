import json
import os
import random
import time
import boto3
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
lambda_client = boto3.client('lambda')


def handler(event, context):
    """
    Main handler for chaos monkey execution.
    """
    
    # Get environment variables
    chaos_interval = int(os.environ.get('CHAOS_INTERVAL', 60))
    target_resource_types = os.environ.get('TARGET_RESOURCE_TYPES', '').split(',')
    protected_resources = os.environ.get('PROTECTED_RESOURCES', '').split(',')
    max_destructions = int(os.environ.get('MAX_DESTRUCTIONS_PER_CYCLE', 1))
    dry_run = os.environ.get('DRY_RUN', 'false').lower() == 'true'
    
    logger.info(f"Chaos Monkey Execution Started")
    logger.info(f"Dry Run Mode: {dry_run}")
    logger.info(f"Target Resource Types: {target_resource_types}")
    logger.info(f"Protected Resources: {protected_resources}")
    logger.info(f"Max Destructions per Cycle: {max_destructions}")
    
    # Track destructions
    destructions_count = 0
    chaos_results = []
    
    try:
        # Chaos for EC2 instances
        if 'aws_instance' in target_resource_types and destructions_count < max_destructions:
            ec2_results = chaos_ec2_instances(protected_resources, max_destructions - destructions_count, dry_run)
            chaos_results.extend(ec2_results)
            destructions_count += len([r for r in ec2_results if r['action'] == 'destroyed'])
        
        # Chaos for RDS instances
        if 'aws_rds_instance' in target_resource_types and destructions_count < max_destructions:
            rds_results = chaos_rds_instances(protected_resources, max_destructions - destructions_count, dry_run)
            chaos_results.extend(rds_results)
            destructions_count += len([r for r in rds_results if r['action'] == 'destroyed'])
        
        # Chaos for Lambda functions
        if 'aws_lambda_function' in target_resource_types and destructions_count < max_destructions:
            lambda_results = chaos_lambda_functions(protected_resources, max_destructions - destructions_count, dry_run)
            chaos_results.extend(lambda_results)
            destructions_count += len([r for r in lambda_results if r['action'] == 'destroyed'])
        
        # Log summary
        logger.info(f"Chaos Monkey Execution Completed")
        logger.info(f"Total Actions: {len(chaos_results)}")
        logger.info(f"Destructions: {destructions_count}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Chaos Monkey executed successfully',
                'results': chaos_results,
                'summary': {
                    'total_actions': len(chaos_results),
                    'destructions': destructions_count,
                    'dry_run': dry_run
                }
            })
        }
        
    except Exception as e:
        logger.error(f"Error during chaos execution: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Chaos Monkey execution failed',
                'error': str(e)
            })
        }


def chaos_ec2_instances(protected_resources, max_destructions, dry_run):
    """
    Chaos for EC2 instances - randomly terminate instances.
    """
    results = []
    
    try:
        # Get all running EC2 instances
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                
                # Check if instance is protected
                tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                instance_name = tags.get('Name', instance_id)
                
                if instance_name not in protected_resources:
                    instances.append({
                        'id': instance_id,
                        'name': instance_name,
                        'type': 'aws_instance',
                        'tags': tags
                    })
        
        # Randomly select instances for chaos
        if instances:
            chaos_count = min(max_destructions, len(instances))
            selected_instances = random.sample(instances, chaos_count)
            
            for instance in selected_instances:
                if dry_run:
                    logger.info(f"[DRY RUN] Would terminate EC2 instance: {instance['id']} ({instance['name']})")
                    results.append({
                        'resource_id': instance['id'],
                        'resource_name': instance['name'],
                        'resource_type': 'aws_instance',
                        'action': 'would_destroy',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                else:
                    try:
                        ec2_client.terminate_instances(InstanceIds=[instance['id']])
                        logger.info(f"Terminated EC2 instance: {instance['id']} ({instance['name']})")
                        results.append({
                            'resource_id': instance['id'],
                            'resource_name': instance['name'],
                            'resource_type': 'aws_instance',
                            'action': 'destroyed',
                            'timestamp': datetime.utcnow().isoformat()
                        })
                    except Exception as e:
                        logger.error(f"Failed to terminate EC2 instance {instance['id']}: {str(e)}")
                        results.append({
                            'resource_id': instance['id'],
                            'resource_name': instance['name'],
                            'resource_type': 'aws_instance',
                            'action': 'failed',
                            'error': str(e),
                            'timestamp': datetime.utcnow().isoformat()
                        })
        
    except Exception as e:
        logger.error(f"Error during EC2 chaos: {str(e)}")
        results.append({
            'resource_type': 'aws_instance',
            'action': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        })
    
    return results


def chaos_rds_instances(protected_resources, max_destructions, dry_run):
    """
    Chaos for RDS instances - randomly delete database instances.
    """
    results = []
    
    try:
        # Get all available RDS instances
        response = rds_client.describe_db_instances()
        
        instances = []
        for db_instance in response['DBInstances']:
            db_instance_id = db_instance['DBInstanceIdentifier']
            
            # Check if instance is protected
            if db_instance_id not in protected_resources:
                instances.append({
                    'id': db_instance_id,
                    'type': 'aws_rds_instance',
                    'status': db_instance['DBInstanceStatus']
                })
        
        # Randomly select instances for chaos
        if instances and any(inst['status'] == 'available' for inst in instances):
            available_instances = [inst for inst in instances if inst['status'] == 'available']
            chaos_count = min(max_destructions, len(available_instances))
            selected_instances = random.sample(available_instances, chaos_count)
            
            for instance in selected_instances:
                if dry_run:
                    logger.info(f"[DRY RUN] Would delete RDS instance: {instance['id']}")
                    results.append({
                        'resource_id': instance['id'],
                        'resource_type': 'aws_rds_instance',
                        'action': 'would_destroy',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                else:
                    try:
                        rds_client.delete_db_instance(
                            DBInstanceIdentifier=instance['id'],
                            SkipFinalSnapshot=True,
                            DeleteAutomatedBackups=True
                        )
                        logger.info(f"Deleted RDS instance: {instance['id']}")
                        results.append({
                            'resource_id': instance['id'],
                            'resource_type': 'aws_rds_instance',
                            'action': 'destroyed',
                            'timestamp': datetime.utcnow().isoformat()
                        })
                    except Exception as e:
                        logger.error(f"Failed to delete RDS instance {instance['id']}: {str(e)}")
                        results.append({
                            'resource_id': instance['id'],
                            'resource_type': 'aws_rds_instance',
                            'action': 'failed',
                            'error': str(e),
                            'timestamp': datetime.utcnow().isoformat()
                        })
        
    except Exception as e:
        logger.error(f"Error during RDS chaos: {str(e)}")
        results.append({
            'resource_type': 'aws_rds_instance',
            'action': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        })
    
    return results


def chaos_lambda_functions(protected_resources, max_destructions, dry_run):
    """
    Chaos for Lambda functions - randomly delete functions.
    """
    results = []
    
    try:
        # Get all Lambda functions
        response = lambda_client.list_functions()
        
        functions = []
        for function in response['Functions']:
            function_name = function['FunctionName']
            
            # Skip protected functions and this chaos monkey function
            if function_name not in protected_resources and 'chaos-monkey' not in function_name:
                functions.append({
                    'name': function_name,
                    'type': 'aws_lambda_function'
                })
        
        # Randomly select functions for chaos
        if functions:
            chaos_count = min(max_destructions, len(functions))
            selected_functions = random.sample(functions, chaos_count)
            
            for function in selected_functions:
                if dry_run:
                    logger.info(f"[DRY RUN] Would delete Lambda function: {function['name']}")
                    results.append({
                        'resource_name': function['name'],
                        'resource_type': 'aws_lambda_function',
                        'action': 'would_destroy',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                else:
                    try:
                        lambda_client.delete_function(FunctionName=function['name'])
                        logger.info(f"Deleted Lambda function: {function['name']}")
                        results.append({
                            'resource_name': function['name'],
                            'resource_type': 'aws_lambda_function',
                            'action': 'destroyed',
                            'timestamp': datetime.utcnow().isoformat()
                        })
                    except Exception as e:
                        logger.error(f"Failed to delete Lambda function {function['name']}: {str(e)}")
                        results.append({
                            'resource_name': function['name'],
                            'resource_type': 'aws_lambda_function',
                            'action': 'failed',
                            'error': str(e),
                            'timestamp': datetime.utcnow().isoformat()
                        })
        
    except Exception as e:
        logger.error(f"Error during Lambda chaos: {str(e)}")
        results.append({
            'resource_type': 'aws_lambda_function',
            'action': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        })
    
    return results
