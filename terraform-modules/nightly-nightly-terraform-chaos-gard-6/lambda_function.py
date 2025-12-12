import json
import boto3
import os
import random
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2_client = boto3.client('ec2')
lambda_client = boto3.client('lambda')
rds_client = boto3.client('rds')

CHAOS_LEVEL = os.environ.get('CHAOS_LEVEL', 'medium')

# Mock rationale: Simulate AWS API responses for testing without actual AWS calls
MOCK_EC2_INSTANCES = [
    {'InstanceId': 'i-1234567890abcdef0'},
    {'InstanceId': 'i-1234567890abcdef1'},
    {'InstanceId': 'i-1234567890abcdef2'}
]

MOCK_RDS_INSTANCES = [
    {'DBInstanceIdentifier': 'test-chaos-garden-rds-abc123'}
]

MOCK_LAMBDA_FUNCTIONS = [
    {'FunctionName': 'test-chaos-garden-lambda-1'},
    {'FunctionName': 'test-chaos-garden-lambda-2'}
]


def lambda_handler(event, context):
    """
    Main Lambda handler for chaos scenarios.
    """
    logger.info(f"Chaos level: {CHAOS_LEVEL}")
    logger.info(f"Event: {json.dumps(event)}")
    
    try:
        # Execute chaos scenarios based on level
        if CHAOS_LEVEL == 'high':
            execute_high_chaos()
        elif CHAOS_LEVEL == 'medium':
            execute_medium_chaos()
        else:
            execute_low_chaos()
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Chaos scenario executed successfully'})
        }
    except Exception as e:
        logger.error(f"Error executing chaos scenario: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def execute_low_chaos():
    """
    Execute low-level chaos scenarios.
    """
    logger.info("Executing low chaos scenarios...")
    
    # Simulate high CPU usage on one EC2 instance
    simulate_high_cpu()


def execute_medium_chaos():
    """
    Execute medium-level chaos scenarios.
    """
    logger.info("Executing medium chaos scenarios...")
    
    # Simulate high CPU usage on one EC2 instance
    simulate_high_cpu()
    
    # Trigger Lambda function overload
    trigger_lambda_overload()


def execute_high_chaos():
    """
    Execute high-level chaos scenarios.
    """
    logger.info("Executing high chaos scenarios...")
    
    # Simulate high CPU usage on one EC2 instance
    simulate_high_cpu()
    
    # Trigger Lambda function overload
    trigger_lambda_overload()
    
    # Simulate RDS high CPU
    simulate_rds_high_cpu()


def simulate_high_cpu():
    """
    Simulate high CPU usage on a random EC2 instance.
    """
    logger.info("Simulating high CPU usage on EC2 instance...")
    
    # In a real scenario, this would use AWS Systems Manager to run commands
    # For now, we'll just log the action
    instance = random.choice(MOCK_EC2_INSTANCES)
    logger.info(f"High CPU simulated on instance: {instance['InstanceId']}")


def trigger_lambda_overload():
    """
    Trigger Lambda function overload.
    """
    logger.info("Triggering Lambda function overload...")
    
    # In a real scenario, this would invoke Lambda functions rapidly
    # For now, we'll just log the action
    function = random.choice(MOCK_LAMBDA_FUNCTIONS)
    logger.info(f"Lambda overload triggered on function: {function['FunctionName']}")


def simulate_rds_high_cpu():
    """
    Simulate high CPU usage on RDS instance.
    """
    logger.info("Simulating high CPU usage on RDS instance...")
    
    # In a real scenario, this would run queries to increase CPU usage
    # For now, we'll just log the action
    instance = random.choice(MOCK_RDS_INSTANCES)
    logger.info(f"High CPU simulated on RDS instance: {instance['DBInstanceIdentifier']}")


def get_ec2_instances():
    """
    Get list of EC2 instances (mocked for testing).
    """
    # Mock rationale: Return mock instances for testing without AWS calls
    return MOCK_EC2_INSTANCES


def get_rds_instances():
    """
    Get list of RDS instances (mocked for testing).
    """
    # Mock rationale: Return mock instances for testing without AWS calls
    return MOCK_RDS_INSTANCES


def get_lambda_functions():
    """
    Get list of Lambda functions (mocked for testing).
    """
    # Mock rationale: Return mock functions for testing without AWS calls
    return MOCK_LAMBDA_FUNCTIONS
