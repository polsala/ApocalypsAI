import json
import boto3
import random
import os
import time

def lambda_handler(event, context):
    """
    Chaos Pollinator Lambda Function
    
    This function performs various chaos experiments on AWS resources
    to test the resilience of the chaos garden.
    """
    
    # Initialize AWS clients
    ec2 = boto3.client('ec2')
    cloudwatch = boto3.client('cloudwatch')
    s3 = boto3.client('s3')
    
    garden_name = os.environ.get('GARDEN_NAME', 'chaos-garden')
    instance_id = os.environ.get('INSTANCE_ID', '')
    
    # List of chaos experiments
    chaos_experiments = [
        'terminate_instance',
        'add_network_latency',
        'stress_cpu',
        'create_custom_metric',
        'random_s3_operation'
    ]
    
    # Select a random chaos experiment
    selected_experiment = random.choice(chaos_experiments)
    
    try:
        if selected_experiment == 'terminate_instance' and instance_id:
            result = terminate_instance(ec2, instance_id)
        elif selected_experiment == 'add_network_latency':
            result = add_network_latency()
        elif selected_experiment == 'stress_cpu':
            result = stress_cpu()
        elif selected_experiment == 'create_custom_metric':
            result = create_custom_metric(cloudwatch, garden_name)
        elif selected_experiment == 'random_s3_operation':
            result = random_s3_operation(s3, garden_name)
        else:
            result = {'status': 'skipped', 'reason': 'No valid experiment selected'}
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'experiment': selected_experiment,
                'result': result,
                'garden': garden_name
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'experiment': selected_experiment,
                'garden': garden_name
            })
        }

def terminate_instance(ec2, instance_id):
    """Terminate an EC2 instance (chaos experiment)"""
    try:
        # Check if instance exists and is running
        response = ec2.describe_instances(InstanceIds=[instance_id])
        
        if response['Reservations']:
            state = response['Reservations'][0]['Instances'][0]['State']['Name']
            
            if state == 'running':
                # Terminate the instance
                ec2.terminate_instances(InstanceIds=[instance_id])
                return {
                    'status': 'success',
                    'action': 'terminate_instance',
                    'instance_id': instance_id,
                    'message': 'Chaos experiment: Instance termination initiated'
                }
            else:
                return {
                    'status': 'skipped',
                    'action': 'terminate_instance',
                    'instance_id': instance_id,
                    'reason': f'Instance is in {state} state'
                }
        else:
            return {
                'status': 'error',
                'action': 'terminate_instance',
                'instance_id': instance_id,
                'reason': 'Instance not found'
            }
    except Exception as e:
        return {
            'status': 'error',
            'action': 'terminate_instance',
            'instance_id': instance_id,
            'error': str(e)
        }

def add_network_latency():
    """Simulate network latency (mock chaos experiment)"""
    # In a real scenario, this would use tools like tc (traffic control)
    # For this example, we'll simulate the effect
    latency_ms = random.randint(100, 1000)
    time.sleep(latency_ms / 1000)  # Simulate delay
    
    return {
        'status': 'success',
        'action': 'add_network_latency',
        'latency_ms': latency_ms,
        'message': f'Chaos experiment: Added {latency_ms}ms of network latency'
    }

def stress_cpu():
    """Stress CPU (mock chaos experiment)"""
    # In a real scenario, this would run CPU-intensive tasks
    # For this example, we'll simulate CPU stress
    stress_duration = random.randint(5, 30)
    start_time = time.time()
    
    # Simulate CPU stress
    while time.time() - start_time < stress_duration:
        # Perform some CPU-intensive calculation
        _ = sum(i * i for i in range(10000))
    
    return {
        'status': 'success',
        'action': 'stress_cpu',
        'duration_seconds': stress_duration,
        'message': f'Chaos experiment: CPU stress for {stress_duration} seconds'
    }

def create_custom_metric(cloudwatch, garden_name):
    """Create a custom CloudWatch metric"""
    try:
        chaos_value = random.randint(0, 100)
        
        cloudwatch.put_metric_data(
            Namespace=f'ChaosGarden/{garden_name}',
            MetricData=[
                {
                    'MetricName': 'ChaosLevel',
                    'Value': chaos_value,
                    'Unit': 'None'
                }
            ]
        )
        
        return {
            'status': 'success',
            'action': 'create_custom_metric',
            'chaos_level': chaos_value,
            'namespace': f'ChaosGarden/{garden_name}',
            'message': f'Chaos experiment: Created custom metric with value {chaos_value}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'action': 'create_custom_metric',
            'error': str(e)
        }

def random_s3_operation(s3, garden_name):
    """Perform random S3 operations (chaos experiment)"""
    try:
        # List all S3 buckets in the account
        response = s3.list_buckets()
        
        chaos_garden_buckets = [
            bucket['Name'] for bucket in response['Buckets']
            if garden_name in bucket['Name']
        ]
        
        if not chaos_garden_buckets:
            return {
                'status': 'skipped',
                'action': 'random_s3_operation',
                'reason': 'No chaos garden buckets found'
            }
        
        # Select a random bucket
        selected_bucket = random.choice(chaos_garden_buckets)
        
        # Randomly choose an operation
        operations = ['list_objects', 'create_object', 'delete_object']
        operation = random.choice(operations)
        
        if operation == 'list_objects':
            objects = s3.list_objects_v2(Bucket=selected_bucket)
            object_count = objects.get('KeyCount', 0)
            
            return {
                'status': 'success',
                'action': 'list_objects',
                'bucket': selected_bucket,
                'object_count': object_count,
                'message': f'Chaos experiment: Listed {object_count} objects in {selected_bucket}'
            }
        
        elif operation == 'create_object':
            chaos_data = f"Chaos timestamp: {int(time.time())}\nRandom chaos value: {random.randint(1, 1000)}"
            object_key = f"chaos/chaos-{int(time.time())}.txt"
            
            s3.put_object(
                Bucket=selected_bucket,
                Key=object_key,
                Body=chaos_data.encode('utf-8')
            )
            
            return {
                'status': 'success',
                'action': 'create_object',
                'bucket': selected_bucket,
                'object_key': object_key,
                'message': f'Chaos experiment: Created object {object_key} in {selected_bucket}'
            }
        
        elif operation == 'delete_object':
            # List objects to find one to delete
            objects = s3.list_objects_v2(Bucket=selected_bucket)
            
            if 'Contents' in objects and objects['Contents']:
                object_to_delete = random.choice(objects['Contents'])['Key']
                
                s3.delete_object(Bucket=selected_bucket, Key=object_to_delete)
                
                return {
                    'status': 'success',
                    'action': 'delete_object',
                    'bucket': selected_bucket,
                    'object_key': object_to_delete,
                    'message': f'Chaos experiment: Deleted object {object_key} from {selected_bucket}'
                }
            else:
                return {
                    'status': 'skipped',
                    'action': 'delete_object',
                    'bucket': selected_bucket,
                    'reason': 'No objects to delete'
                }
        
    except Exception as e:
        return {
            'status': 'error',
            'action': 'random_s3_operation',
            'error': str(e)
        }
