import json
import boto3
import random
import os
import logging
import time
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
ec2_client = boto3.client('ec2')
rds_client = boto3.client('rds')
cloudwatch = boto3.client('cloudwatch')


def lambda_handler(event, context):
    """
    Main Lambda handler for chaos monkey functionality.
    
    Args:
        event: CloudWatch Events event
        context: Lambda execution context
    
    Returns:
        dict: Execution result
    """
    try:
        # Get configuration from environment variables
        chaos_probability = float(os.environ.get('CHAOS_PROBABILITY', '0.01'))
        target_resource_types = os.environ.get('TARGET_RESOURCE_TYPES', 'aws_instance').split(',')
        excluded_tags = json.loads(os.environ.get('EXCLUDED_TAGS', '{}'))
        safe_mode = os.environ.get('SAFE_MODE', 'true').lower() == 'true'
        time_window_start = int(os.environ.get('TIME_WINDOW_START', '9'))
        time_window_end = int(os.environ.get('TIME_WINDOW_END', '17'))
        
        # Check if we're in the time window
        current_hour = datetime.now().hour
        if not (time_window_start <= current_hour <= time_window_end):
            logger.info(f"Outside time window ({time_window_start}-{time_window_end}). Skipping chaos.")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Outside time window, no chaos executed'})
            }
        
        # Decide if chaos should happen
        if not should_execute_chaos(chaos_probability):
            logger.info(f"Chaos probability {chaos_probability} not met. No chaos this time.")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Chaos probability not met'})
            }
        
        # Execute chaos
        chaos_result = execute_chaos(target_resource_types, excluded_tags, safe_mode)
        
        # Send metrics to CloudWatch
        send_chaos_metrics(chaos_result)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Chaos executed successfully',
                'result': chaos_result
            })
        }
        
    except Exception as e:
        logger.error(f"Error executing chaos: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def should_execute_chaos(probability):
    """
    Determine if chaos should be executed based on probability.
    
    Args:
        probability (float): Probability of chaos (0.0 to 1.0)
    
    Returns:
        bool: True if chaos should execute
    """
    random_value = random.random()
    logger.info(f"Random value: {random_value}, Probability threshold: {probability}")
    return random_value < probability


def execute_chaos(target_resource_types, excluded_tags, safe_mode):
    """
    Execute chaos by terminating random resources.
    
    Args:
        target_resource_types (list): List of resource types to target
        excluded_tags (dict): Tags that exclude resources from chaos
        safe_mode (bool): Whether to run in safe mode (dry run)
    
    Returns:
        dict: Result of chaos execution
    """
    chaos_result = {
        'resources_targeted': [],
        'resources_terminated': [],
        'resources_skipped': [],
        'errors': []
    }
    
    for resource_type in target_resource_types:
        try:
            if resource_type == 'aws_instance':
                result = chaos_ec2_instances(excluded_tags, safe_mode)
            elif resource_type == 'aws_rds_instance':
                result = chaos_rds_instances(excluded_tags, safe_mode)
            else:
                logger.warning(f"Unknown resource type: {resource_type}")
                continue
                
            chaos_result['resources_targeted'].extend(result.get('resources_targeted', []))
            chaos_result['resources_terminated'].extend(result.get('resources_terminated', []))
            chaos_result['resources_skipped'].extend(result.get('resources_skipped', []))
            chaos_result['errors'].extend(result.get('errors', []))
            
        except Exception as e:
            error_msg = f"Error during chaos for {resource_type}: {str(e)}"
            logger.error(error_msg)
            chaos_result['errors'].append(error_msg)
    
    # Log summary
    logger.info(f"Chaos execution summary: {len(chaos_result['resources_terminated'])} resources terminated, "
                f"{len(chaos_result['resources_skipped'])} skipped, {len(chaos_result['errors'])} errors")
    
    return chaos_result


def chaos_ec2_instances(excluded_tags, safe_mode):
    """
    Execute chaos on EC2 instances.
    
    Args:
        excluded_tags (dict): Tags that exclude instances from chaos
        safe_mode (bool): Whether to run in safe mode
    
    Returns:
        dict: Result of EC2 chaos execution
    """
    result = {
        'resources_targeted': [],
        'resources_terminated': [],
        'resources_skipped': [],
        'errors': []
    }
    
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
                instances.append(instance)
        
        if not instances:
            logger.info("No running EC2 instances found")
            return result
        
        # Filter instances based on excluded tags
        targetable_instances = []
        for instance in instances:
            instance_tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
            
            # Check if instance should be excluded
            excluded = False
            for key, value in excluded_tags.items():
                if instance_tags.get(key) == value:
                    excluded = True
                    break
            
            if not excluded:
                targetable_instances.append(instance)
        
        if not targetable_instances:
            logger.info("No targetable EC2 instances found (all excluded by tags)")
            return result
        
        # Select random instance to terminate
        target_instance = random.choice(targetable_instances)
        instance_id = target_instance['InstanceId']
        
        result['resources_targeted'].append({
            'type': 'aws_instance',
            'id': instance_id,
            'tags': {tag['Key']: tag['Value'] for tag in target_instance.get('Tags', [])}
        })
        
        if safe_mode:
            logger.info(f"[SAFE MODE] Would terminate EC2 instance: {instance_id}")
            result['resources_skipped'].append({
                'type': 'aws_instance',
                'id': instance_id,
                'reason': 'safe_mode'
            })
        else:
            try:
                ec2_client.terminate_instances(InstanceIds=[instance_id])
                logger.info(f"Terminated EC2 instance: {instance_id}")
                result['resources_terminated'].append({
                    'type': 'aws_instance',
                    'id': instance_id
                })
                
                # Wait a bit for the termination to be processed
                time.sleep(2)
                
            except Exception as e:
                error_msg = f"Failed to terminate EC2 instance {instance_id}: {str(e)}"
                logger.error(error_msg)
                result['errors'].append(error_msg)
                
    except Exception as e:
        error_msg = f"Error during EC2 chaos: {str(e)}"
        logger.error(error_msg)
        result['errors'].append(error_msg)
    
    return result


def chaos_rds_instances(excluded_tags, safe_mode):
    """
    Execute chaos on RDS instances.
    
    Args:
        excluded_tags (dict): Tags that exclude instances from chaos
        safe_mode (bool): Whether to run in safe mode
    
    Returns:
        dict: Result of RDS chaos execution
    """
    result = {
        'resources_targeted': [],
        'resources_terminated': [],
        'resources_skipped': [],
        'errors': []
    }
    
    try:
        # Get all available RDS instances
        response = rds_client.describe_db_instances()
        
        db_instances = response['DBInstances']
        
        if not db_instances:
            logger.info("No RDS instances found")
            return result
        
        # Filter instances based on excluded tags and state
        targetable_instances = []
        for db_instance in db_instances:
            if db_instance['DBInstanceStatus'] != 'available':
                continue
                
            # Get instance tags
            arn = db_instance['DBInstanceArn']
            tag_response = rds_client.list_tags_for_resource(ResourceName=arn)
            instance_tags = {tag['Key']: tag['Value'] for tag in tag_response['TagList']}
            
            # Check if instance should be excluded
            excluded = False
            for key, value in excluded_tags.items():
                if instance_tags.get(key) == value:
                    excluded = True
                    break
            
            if not excluded:
                targetable_instances.append({
                    'instance': db_instance,
                    'tags': instance_tags
                })
        
        if not targetable_instances:
            logger.info("No targetable RDS instances found (all excluded by tags or not available)")
            return result
        
        # Select random instance to terminate
        target_instance_data = random.choice(targetable_instances)
        target_instance = target_instance_data['instance']
        db_instance_identifier = target_instance['DBInstanceIdentifier']
        
        result['resources_targeted'].append({
            'type': 'aws_rds_instance',
            'id': db_instance_identifier,
            'tags': target_instance_data['tags']
        })
        
        if safe_mode:
            logger.info(f"[SAFE MODE] Would delete RDS instance: {db_instance_identifier}")
            result['resources_skipped'].append({
                'type': 'aws_rds_instance',
                'id': db_instance_identifier,
                'reason': 'safe_mode'
            })
        else:
            try:
                # Delete the RDS instance
                rds_client.delete_db_instance(
                    DBInstanceIdentifier=db_instance_identifier,
                    SkipFinalSnapshot=True,
                    DeleteAutomatedBackups=True
                )
                logger.info(f"Deleted RDS instance: {db_instance_identifier}")
                result['resources_terminated'].append({
                    'type': 'aws_rds_instance',
                    'id': db_instance_identifier
                })
                
            except Exception as e:
                error_msg = f"Failed to delete RDS instance {db_instance_identifier}: {str(e)}"
                logger.error(error_msg)
                result['errors'].append(error_msg)
                
    except Exception as e:
        error_msg = f"Error during RDS chaos: {str(e)}"
        logger.error(error_msg)
        result['errors'].append(error_msg)
    
    return result


def send_chaos_metrics(result):
    """
    Send chaos execution metrics to CloudWatch.
    
    Args:
        result (dict): Chaos execution result
    """
    try:
        # Send metrics to CloudWatch
        metrics_data = [
            {
                'MetricName': 'ChaosEvents',
                'Value': 1,
                'Unit': 'Count'
            },
            {
                'MetricName': 'ResourcesTerminated',
                'Value': len(result['resources_terminated']),
                'Unit': 'Count'
            },
            {
                'MetricName': 'ResourcesSkipped',
                'Value': len(result['resources_skipped']),
                'Unit': 'Count'
            },
            {
                'MetricName': 'Errors',
                'Value': len(result['errors']),
                'Unit': 'Count'
            }
        ]
        
        cloudwatch.put_metric_data(
            Namespace='ChaosMonkey',
            MetricData=metrics_data
        )
        
        logger.info("Successfully sent chaos metrics to CloudWatch")
        
    except Exception as e:
        logger.error(f"Failed to send metrics to CloudWatch: {str(e)}")
