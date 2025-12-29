import json
import os
import random
import boto3
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')


class ChaosMonkey:
    def __init__(self):
        self.destruction_probability = float(os.environ.get('DESTRUCTION_PROBABILITY', 0.05))
        self.target_resource_types = os.environ.get('TARGET_RESOURCE_TYPES', '').split(',')
        self.safe_mode = os.environ.get('SAFE_MODE', 'true').lower() == 'true'
        self.max_resources_per_run = int(os.environ.get('MAX_RESOURCES_PER_RUN', 3))
        self.excluded_resources = os.environ.get('EXCLUDED_RESOURCES', '').split(',')
        self.aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        
        # Remove empty strings from excluded resources
        self.excluded_resources = [r for r in self.excluded_resources if r.strip()]
        
        logger.info(f"Chaos Monkey initialized with:")
        logger.info(f"  - Destruction probability: {self.destruction_probability}")
        logger.info(f"  - Target types: {self.target_resource_types}")
        logger.info(f"  - Safe mode: {self.safe_mode}")
        logger.info(f"  - Max resources per run: {self.max_resources_per_run}")
        logger.info(f"  - Excluded resources: {self.excluded_resources}")
    
    def should_execute_chaos(self) -> bool:
        """Determine if chaos should be executed based on probability"""
        random_value = random.random()
        should_execute = random_value < self.destruction_probability
        
        logger.info(f"Random value: {random_value}, Threshold: {self.destruction_probability}, Execute: {should_execute}")
        return should_execute
    
    def get_targetable_resources(self) -> List[Dict[str, Any]]:
        """Discover resources that can be targeted for chaos"""
        resources = []
        
        if 'aws_instance' in self.target_resource_types:
            resources.extend(self._get_ec2_instances())
        
        if 'aws_rds_instance' in self.target_resource_types:
            resources.extend(self._get_rds_instances())
        
        if 'aws_s3_bucket' in self.target_resource_types:
            resources.extend(self._get_s3_buckets())
        
        if 'aws_lambda_function' in self.target_resource_types:
            resources.extend(self._get_lambda_functions())
        
        # Filter out excluded resources
        filtered_resources = []
        for resource in resources:
            if resource['id'] not in self.excluded_resources:
                filtered_resources.append(resource)
        
        logger.info(f"Found {len(filtered_resources)} targetable resources out of {len(resources)} discovered")
        return filtered_resources
    
    def _get_ec2_instances(self) -> List[Dict[str, Any]]:
        """Get running EC2 instances"""
        try:
            response = ec2_client.describe_instances(
                Filters=[
                    {'Name': 'instance-state-name', 'Values': ['running']}
                ]
            )
            
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    # Skip if instance is excluded
                    if instance['InstanceId'] in self.excluded_resources:
                        continue
                    
                    # Skip if instance has a 'chaos-monkey-exclude' tag
                    tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    if tags.get('chaos-monkey-exclude', 'false').lower() == 'true':
                        continue
                    
                    instances.append({
                        'id': instance['InstanceId'],
                        'type': 'aws_instance',
                        'name': tags.get('Name', instance['InstanceId']),
                        'state': instance['State']['Name'],
                        'launch_time': instance['LaunchTime'].isoformat()
                    })
            
            logger.info(f"Found {len(instances)} EC2 instances")
            return instances
        except Exception as e:
            logger.error(f"Error getting EC2 instances: {e}")
            return []
    
    def _get_rds_instances(self) -> List[Dict[str, Any]]:
        """Get RDS instances"""
        try:
            response = rds_client.describe_db_instances()
            
            instances = []
            for db_instance in response['DBInstances']:
                # Skip if instance is excluded
                if db_instance['DBInstanceIdentifier'] in self.excluded_resources:
                    continue
                
                # Skip if instance has a 'chaos-monkey-exclude' tag
                tags_response = rds_client.list_tags_for_resource(
                    ResourceName=db_instance['DBInstanceArn']
                )
                tags = {tag['Key']: tag['Value'] for tag in tags_response['TagList']}
                if tags.get('chaos-monkey-exclude', 'false').lower() == 'true':
                    continue
                
                instances.append({
                    'id': db_instance['DBInstanceIdentifier'],
                    'type': 'aws_rds_instance',
                    'name': db_instance['DBInstanceIdentifier'],
                    'state': db_instance['DBInstanceStatus'],
                    'engine': db_instance['Engine'],
                    'size': db_instance.get('AllocatedStorage', 0)
                })
            
            logger.info(f"Found {len(instances)} RDS instances")
            return instances
        except Exception as e:
            logger.error(f"Error getting RDS instances: {e}")
            return []
    
    def _get_s3_buckets(self) -> List[Dict[str, Any]]:
        """Get S3 buckets"""
        try:
            response = s3_client.list_buckets()
            
            buckets = []
            for bucket in response['Buckets']:
                # Skip if bucket is excluded
                if bucket['Name'] in self.excluded_resources:
                    continue
                
                # Skip if bucket has a 'chaos-monkey-exclude' tag
                try:
                    tags_response = s3_client.get_bucket_tagging(Bucket=bucket['Name'])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['TagSet']}
                    if tags.get('chaos-monkey-exclude', 'false').lower() == 'true':
                        continue
                except:
                    # No tags or error getting tags - continue
                    pass
                
                buckets.append({
                    'id': bucket['Name'],
                    'type': 'aws_s3_bucket',
                    'name': bucket['Name'],
                    'creation_date': bucket['CreationDate'].isoformat()
                })
            
            logger.info(f"Found {len(buckets)} S3 buckets")
            return buckets
        except Exception as e:
            logger.error(f"Error getting S3 buckets: {e}")
            return []
    
    def _get_lambda_functions(self) -> List[Dict[str, Any]]:
        """Get Lambda functions"""
        try:
            response = lambda_client.list_functions()
            
            functions = []
            for function in response['Functions']:
                # Skip if function is excluded
                if function['FunctionName'] in self.excluded_resources:
                    continue
                
                # Skip if function has a 'chaos-monkey-exclude' tag
                tags_response = lambda_client.list_tags(
                    Resource=function['FunctionArn']
                )
                tags = tags_response.get('Tags', {})
                if tags.get('chaos-monkey-exclude', 'false').lower() == 'true':
                    continue
                
                functions.append({
                    'id': function['FunctionName'],
                    'type': 'aws_lambda_function',
                    'name': function['FunctionName'],
                    'runtime': function['Runtime'],
                    'memory_size': function['MemorySize']
                })
            
            logger.info(f"Found {len(functions)} Lambda functions")
            return functions
        except Exception as e:
            logger.error(f"Error getting Lambda functions: {e}")
            return []
    
    def select_resources_for_chaos(self, resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Randomly select resources for chaos based on configured limits"""
        if not resources:
            return []
        
        # Determine how many resources to target (up to max_resources_per_run)
        max_to_target = min(self.max_resources_per_run, len(resources))
        
        # Randomly select resources
        selected_count = random.randint(1, max_to_target) if max_to_target > 0 else 0
        selected_resources = random.sample(resources, selected_count)
        
        logger.info(f"Selected {len(selected_resources)} resources for chaos out of {len(resources)} available")
        return selected_resources
    
    def destroy_resource(self, resource: Dict[str, Any]) -> Dict[str, Any]:
        """Destroy a single resource"""
        result = {
            'resource': resource,
            'action': 'destroy',
            'success': False,
            'error': None,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        try:
            if resource['type'] == 'aws_instance':
                self._destroy_ec2_instance(resource['id'], result)
            elif resource['type'] == 'aws_rds_instance':
                self._destroy_rds_instance(resource['id'], result)
            elif resource['type'] == 'aws_s3_bucket':
                self._destroy_s3_bucket(resource['id'], result)
            elif resource['type'] == 'aws_lambda_function':
                self._destroy_lambda_function(resource['id'], result)
            else:
                result['error'] = f"Unknown resource type: {resource['type']}"
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Error destroying resource {resource['id']}: {e}")
        
        return result
    
    def _destroy_ec2_instance(self, instance_id: str, result: Dict[str, Any]):
        """Destroy an EC2 instance"""
        if self.safe_mode:
            logger.info(f"[SAFE MODE] Would terminate EC2 instance: {instance_id}")
            result['success'] = True
            result['message'] = f"[SAFE MODE] Would terminate EC2 instance: {instance_id}"
            return
        
        # Stop the instance first
        ec2_client.stop_instances(InstanceIds=[instance_id])
        
        # Wait for instance to stop
        waiter = ec2_client.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[instance_id])
        
        # Terminate the instance
        ec2_client.terminate_instances(InstanceIds=[instance_id])
        
        result['success'] = True
        result['message'] = f"Terminated EC2 instance: {instance_id}"
        logger.info(result['message'])
    
    def _destroy_rds_instance(self, db_instance_id: str, result: Dict[str, Any]):
        """Destroy an RDS instance"""
        if self.safe_mode:
            logger.info(f"[SAFE MODE] Would delete RDS instance: {db_instance_id}")
            result['success'] = True
            result['message'] = f"[SAFE MODE] Would delete RDS instance: {db_instance_id}"
            return
        
        # Delete the RDS instance
        rds_client.delete_db_instance(
            DBInstanceIdentifier=db_instance_id,
            SkipFinalSnapshot=True,
            DeleteAutomatedBackups=True
        )
        
        result['success'] = True
        result['message'] = f"Deleted RDS instance: {db_instance_id}"
        logger.info(result['message'])
    
    def _destroy_s3_bucket(self, bucket_name: str, result: Dict[str, Any]):
        """Destroy an S3 bucket"""
        if self.safe_mode:
            logger.info(f"[SAFE MODE] Would delete S3 bucket: {bucket_name}")
            result['success'] = True
            result['message'] = f"[SAFE MODE] Would delete S3 bucket: {bucket_name}"
            return
        
        # Delete all objects in the bucket first
        try:
            # List and delete all objects
            objects = s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in objects:
                delete_keys = [{'Key': obj['Key']} for obj in objects['Contents']]
                s3_client.delete_objects(
                    Bucket=bucket_name,
                    Delete={'Objects': delete_keys}
                )
            
            # Delete the bucket
            s3_client.delete_bucket(Bucket=bucket_name)
            
            result['success'] = True
            result['message'] = f"Deleted S3 bucket: {bucket_name}"
            logger.info(result['message'])
        except Exception as e:
            result['error'] = str(e)
            logger.error(f"Error deleting S3 bucket {bucket_name}: {e}")
    
    def _destroy_lambda_function(self, function_name: str, result: Dict[str, Any]):
        """Destroy a Lambda function"""
        if self.safe_mode:
            logger.info(f"[SAFE MODE] Would delete Lambda function: {function_name}")
            result['success'] = True
            result['message'] = f"[SAFE MODE] Would delete Lambda function: {function_name}"
            return
        
        # Delete the Lambda function
        lambda_client.delete_function(FunctionName=function_name)
        
        result['success'] = True
        result['message'] = f"Deleted Lambda function: {function_name}"
        logger.info(result['message'])
    
    def execute_chaos(self) -> Dict[str, Any]:
        """Execute the chaos monkey"""
        logger.info("Starting chaos monkey execution")
        
        # Check if we should execute chaos
        if not self.should_execute_chaos():
            logger.info("Chaos execution skipped based on probability")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'executed': False,
                'reason': 'Probability threshold not met',
                'safe_mode': self.safe_mode
            }
        
        # Get targetable resources
        resources = self.get_targetable_resources()
        
        if not resources:
            logger.info("No targetable resources found")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'executed': True,
                'resources_found': 0,
                'resources_destroyed': 0,
                'safe_mode': self.safe_mode
            }
        
        # Select resources for chaos
        selected_resources = self.select_resources_for_chaos(resources)
        
        if not selected_resources:
            logger.info("No resources selected for destruction")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'executed': True,
                'resources_found': len(resources),
                'resources_selected': 0,
                'resources_destroyed': 0,
                'safe_mode': self.safe_mode
            }
        
        # Execute destruction
        results = []
        destroyed_count = 0
        
        for resource in selected_resources:
            logger.info(f"Destroying resource: {resource['id']} ({resource['type']})")
            result = self.destroy_resource(resource)
            results.append(result)
            
            if result['success']:
                destroyed_count += 1
        
        # Log summary
        summary = {
            'timestamp': datetime.utcnow().isoformat(),
            'executed': True,
            'resources_found': len(resources),
            'resources_selected': len(selected_resources),
            'resources_destroyed': destroyed_count,
            'safe_mode': self.safe_mode,
            'destruction_probability': self.destruction_probability,
            'target_types': self.target_resource_types,
            'excluded_resources': self.excluded_resources
        }
        
        logger.info(f"Chaos execution completed: {destroyed_count}/{len(selected_resources)} resources destroyed")
        
        return summary


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda function handler for chaos monkey execution
    
    Args:
        event: Lambda event object
        context: Lambda context object
    
    Returns:
        Dict containing execution results
    """
    try:
        logger.info(f"Chaos Monkey execution started at {datetime.utcnow().isoformat()}")
        logger.info(f"Event: {json.dumps(event)}")
        
        # Initialize chaos monkey
        chaos_monkey = ChaosMonkey()
        
        # Execute chaos
        result = chaos_monkey.execute_chaos()
        
        logger.info(f"Chaos Monkey execution completed: {json.dumps(result)}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(result, indent=2)
        }
        
    except Exception as e:
        logger.error(f"Chaos Monkey execution failed: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            })
        }


if __name__ == "__main__":
    # For local testing
    import sys
    
    # Mock environment variables for local testing
    os.environ['DESTRUCTION_PROBABILITY'] = '1.0'  # Always execute for testing
    os.environ['TARGET_RESOURCE_TYPES'] = 'aws_instance,aws_rds_instance'
    os.environ['SAFE_MODE'] = 'true'
    os.environ['MAX_RESOURCES_PER_RUN'] = '2'
    os.environ['EXCLUDED_RESOURCES'] = ''
    os.environ['AWS_REGION'] = 'us-east-1'
    
    # Mock event
    test_event = {
        'source': 'aws.events',
        'detail-type': 'Scheduled Event',
        'resources': ['arn:aws:events:us-east-1:123456789012:rule/chaos-monkey-schedule-test']
    }
    
    # Execute
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))
