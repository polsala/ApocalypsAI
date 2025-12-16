import json
import boto3
import random
import time
import os
import logging
from datetime import datetime, timedelta

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')
ec2_client = boto3.client('ec2')
cloudwatch_client = boto3.client('cloudwatch')

# Configuration from environment variables
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'staging')
REGION = os.environ.get('REGION', 'us-west-2')
CHAOS_SCENARIOS = os.environ.get('CHAOS_SCENARIOS', '').split(',')
EXPERIMENT_DURATION = os.environ.get('EXPERIMENT_DURATION', '30m')
MAX_EXPERIMENTS = int(os.environ.get('MAX_EXPERIMENTS', '3'))
ROLLBACK_ENABLED = os.environ.get('ROLLBACK_ENABLED', 'true').lower() == 'true'
LOG_BUCKET = os.environ.get('LOG_BUCKET', '')

# Whimsical chaos experiment names
CHAOS_NAMES = [
    "Chaos Goblin", "Entropy Sprite", "Mayhem Pixie", "Disorder Djinn",
    "Bedlam Basilisk", "Pandemonium Pegasus", "Anarchy Angel",
    "Confusion Chimera", "Turbulence Troll", "Upheaval Unicorn",
    "Ruckus Roc", "Havoc Hydra", "Frenzy Fairy", "Catastrophe Cat",
    "Disarray Dragon", "Mischief Manticore", "Rompus Roc", "Spectacle Sphinx"
]

# Chaos scenarios
CHAOS_FUNCTIONS = {
    "network_latency": None,  # Will be set dynamically
    "resource_deletion": None,
    "service_disruption": None
}


def log_experiment(experiment_data):
    """Log experiment data to S3"""
    if not LOG_BUCKET:
        return
    
    timestamp = datetime.now().isoformat()
    key = f"experiments/{timestamp}_{experiment_data['name'].replace(' ', '_')}.json"
    
    try:
        s3_client.put_object(
            Bucket=LOG_BUCKET,
            Key=key,
            Body=json.dumps(experiment_data, indent=2, default=str)
        )
        logger.info(f"Experiment logged to s3://{LOG_BUCKET}/{key}")
    except Exception as e:
        logger.error(f"Failed to log experiment: {str(e)}")


def put_metric(metric_name, value, dimensions=None):
    """Put a custom metric to CloudWatch"""
    if not dimensions:
        dimensions = [{'Name': 'Environment', 'Value': ENVIRONMENT}]
    
    try:
        cloudwatch_client.put_metric_data(
            Namespace='ChaosEngineering',
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': dimensions,
                    'Timestamp': datetime.now(),
                    'Value': value,
                    'Unit': 'Count'
                }
            ]
        )
    except Exception as e:
        logger.error(f"Failed to put metric {metric_name}: {str(e)}")


def get_random_chaos_name():
    """Get a random whimsical chaos experiment name"""
    return random.choice(CHAOS_NAMES)


def get_target_instances():
    """Get instances tagged for chaos experiments"""
    try:
        response = ec2_client.describe_instances(
            Filters=[
                {'Name': 'tag:ChaosTarget', 'Values': ['true']},
                {'Name': 'tag:Environment', 'Values': [ENVIRONMENT]},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance['InstanceId'])
        
        return instances
    except Exception as e:
        logger.error(f"Failed to get target instances: {str(e)}")
        return []


def chaos_network_latency(instance_id):
    """Add network latency to an instance"""
    try:
        # This is a simplified example - in reality, you'd use tc or similar tools
        # For demo purposes, we'll just log the action
        logger.info(f"Adding network latency to instance {instance_id}")
        
        # Simulate network latency by creating a network ACL entry
        response = ec2_client.describe_network_interfaces(
            Filters=[
                {'Name': 'attachment.instance-id', 'Values': [instance_id]}
            ]
        )
        
        if response['NetworkInterfaces']:
            eni_id = response['NetworkInterfaces'][0]['NetworkInterfaceId']
            logger.info(f"Would add latency to ENI {eni_id}")
            
        return True
    except Exception as e:
        logger.error(f"Failed to add network latency: {str(e)}")
        return False


def chaos_resource_deletion(instance_id):
    """Simulate resource deletion by stopping an instance"""
    try:
        logger.info(f"Stopping instance {instance_id} for chaos experiment")
        ec2_client.stop_instances(InstanceIds=[instance_id])
        
        # Wait a bit then start it again
        time.sleep(30)
        ec2_client.start_instances(InstanceIds=[instance_id])
        
        return True
    except Exception as e:
        logger.error(f"Failed to stop/start instance: {str(e)}")
        return False


def chaos_service_disruption(instance_id):
    """Simulate service disruption by rebooting an instance"""
    try:
        logger.info(f"Rebooting instance {instance_id} for chaos experiment")
        ec2_client.reboot_instances(InstanceIds=[instance_id])
        return True
    except Exception as e:
        logger.error(f"Failed to reboot instance: {str(e)}")
        return False


def execute_chaos_experiment(scenario, instance_id):
    """Execute a specific chaos experiment"""
    chaos_functions = {
        "network_latency": chaos_network_latency,
        "resource_deletion": chaos_resource_deletion,
        "service_disruption": chaos_service_disruption
    }
    
    if scenario not in chaos_functions:
        logger.error(f"Unknown chaos scenario: {scenario}")
        return False
    
    logger.info(f"Executing {scenario} on instance {instance_id}")
    
    start_time = datetime.now()
    success = chaos_functions[scenario](instance_id)
    end_time = datetime.now()
    
    experiment_data = {
        'name': get_random_chaos_name(),
        'scenario': scenario,
        'instance_id': instance_id,
        'start_time': start_time,
        'end_time': end_time,
        'success': success,
        'duration': str(end_time - start_time),
        'environment': ENVIRONMENT,
        'region': REGION
    }
    
    log_experiment(experiment_data)
    put_metric('ChaosExperimentExecuted', 1)
    
    if not success:
        put_metric('ChaosExperimentFailures', 1)
    
    return success


def lambda_handler(event, context):
    """Main Lambda handler for chaos orchestration"""
    logger.info(f"Starting chaos experiment in {ENVIRONMENT} environment")
    
    # Get target instances
    target_instances = get_target_instances()
    
    if not target_instances:
        logger.info("No target instances found for chaos experiments")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'No target instances found',
                'environment': ENVIRONMENT
            })
        }
    
    logger.info(f"Found {len(target_instances)} target instances: {target_instances}")
    
    # Execute chaos experiments
    experiments_run = 0
    experiments_success = 0
    
    for instance_id in target_instances[:MAX_EXPERIMENTS]:
        for scenario in CHAOS_SCENARIOS:
            if experiments_run >= MAX_EXPERIMENTS:
                break
            
            success = execute_chaos_experiment(scenario, instance_id)
            experiments_run += 1
            
            if success:
                experiments_success += 1
            
            # Small delay between experiments
            time.sleep(5)
        
        if experiments_run >= MAX_EXPERIMENTS:
            break
    
    # Log summary
    summary = {
        'environment': ENVIRONMENT,
        'region': REGION,
        'experiments_run': experiments_run,
        'experiments_success': experiments_success,
        'success_rate': experiments_success / experiments_run if experiments_run > 0 else 0,
        'timestamp': datetime.now().isoformat()
    }
    
    logger.info(f"Chaos experiment summary: {json.dumps(summary, indent=2)}")
    log_experiment(summary)
    
    # Put summary metrics
    put_metric('ChaosExperimentsRun', experiments_run)
    put_metric('ChaosExperimentsSuccess', experiments_success)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Chaos experiments completed',
            'summary': summary,
            'environment': ENVIRONMENT
        })
    }


def api_handler(event, context):
    """API Gateway handler for chaos garden dashboard"""
    http_method = event.get('httpMethod', '')
    
    if http_method == 'GET':
        # Return current chaos garden status
        target_instances = get_target_instances()
        
        response = {
            'chaos_garden_name': f"{get_random_chaos_name()}'s Chaos Garden",
            'environment': ENVIRONMENT,
            'region': REGION,
            'target_instances_count': len(target_instances),
            'target_instances': target_instances,
            'enabled_scenarios': CHAOS_SCENARIOS,
            'max_concurrent_experiments': MAX_EXPERIMENTS,
            'rollback_enabled': ROLLBACK_ENABLED,
            'experiment_duration': EXPERIMENT_DURATION,
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response, indent=2)
        }
    
    elif http_method == 'POST':
        # Trigger chaos experiments manually
        body = json.loads(event.get('body', '{}'))
        scenario = body.get('scenario', 'network_latency')
        instance_id = body.get('instance_id')
        
        if not instance_id:
            target_instances = get_target_instances()
            if not target_instances:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'No target instances available'})
                }
            instance_id = target_instances[0]
        
        success = execute_chaos_experiment(scenario, instance_id)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Manual chaos experiment triggered',
                'scenario': scenario,
                'instance_id': instance_id,
                'success': success,
                'environment': ENVIRONMENT
            })
        }
    
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
