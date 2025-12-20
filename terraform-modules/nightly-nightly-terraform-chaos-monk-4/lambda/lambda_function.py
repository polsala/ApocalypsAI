import json
import boto3
import os
import logging
import random
import time
from datetime import datetime, timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')
cloudwatch = boto3.client('cloudwatch')

# Environment variables
LOG_GROUP_NAME = os.environ.get('LOG_GROUP_NAME', '/apocalypsaid/chaos-monkey')
LOG_STREAM_NAME = os.environ.get('LOG_STREAM_NAME', 'chaos-events')
CHAOS_LEVEL = os.environ.get('CHAOS_LEVEL', 'medium')
DRY_RUN = os.environ.get('DRY_RUN', 'false').lower() == 'true'
MIN_INSTANCE_COUNT = int(os.environ.get('MIN_INSTANCE_COUNT', '1'))

# Chaos probabilities by level
CHAOS_PROBABILITIES = {
    'gentle': 1,
    'medium': 5,
    'extreme': 15
}

# Chaos types and their implementations
CHAOS_TYPES = {
    'instance_termination': 'terminate_instance',
    'instance_stop': 'stop_instance',
    'network_latency': 'introduce_network_latency',
    'cpu_stress': 'stress_cpu',
    'memory_stress': 'stress_memory',
    'disk_io_stress': 'stress_disk_io'
}


class ChaosMonkey:
    def __init__(self):
        self.chaos_level = CHAOS_LEVEL
        self.dry_run = DRY_RUN
        self.min_instance_count = MIN_INSTANCE_COUNT
        self.probability = CHAOS_PROBABILITIES.get(self.chaos_level, 5)
    
    def should_trigger_chaos(self):
        """Determine if chaos should be triggered based on probability."""
        return random.randint(1, 100) <= self.probability
    
    def get_target_instances(self):
        """Get list of target EC2 instances."""
        try:
            response = ec2.describe_instances(
                Filters=[
                    {'Name': 'instance-state-name', 'Values': ['running']}
                ]
            )
            
            instances = []
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    # Skip instances with excluded tags
                    if self._has_excluded_tags(instance):
                        continue
                    
                    # Only include instances with included tags (if specified)
                    if not self._matches_included_tags(instance):
                        continue
                    
                    instances.append(instance['InstanceId'])
            
            # Ensure we don't go below minimum instance count
            if len(instances) <= self.min_instance_count:
                return []
            
            return instances
            
        except Exception as e:
            logger.error(f"Error getting target instances: {e}")
            return []
    
    def _has_excluded_tags(self, instance):
        """Check if instance has excluded tags."""
        excluded_tags = os.environ.get('EXCLUDED_TAGS', '').split(',')
        if not excluded_tags or excluded_tags == ['']:
            return False
        
        instance_tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
        
        for tag in excluded_tags:
            if tag in instance_tags:
                return True
        
        return False
    
    def _matches_included_tags(self, instance):
        """Check if instance matches included tags."""
        included_tags_str = os.environ.get('INCLUDED_TAGS', '')
        if not included_tags_str:
            return True
        
        try:
            included_tags = json.loads(included_tags_str)
        except:
            return True
        
        instance_tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
        
        for key, value in included_tags.items():
            if instance_tags.get(key) != value:
                return False
        
        return True
    
    def select_chaos_type(self):
        """Select a random chaos type."""
        chaos_types = list(CHAOS_TYPES.keys())
        return random.choice(chaos_types)
    
    def execute_chaos(self, instance_id, chaos_type):
        """Execute the selected chaos type on the target instance."""
        logger.info(f"Executing {chaos_type} on instance {instance_id}")
        
        if self.dry_run:
            logger.info(f"[DRY RUN] Would execute {chaos_type} on instance {instance_id}")
            return True, None
        
        try:
            if chaos_type == 'instance_termination':
                return self.terminate_instance(instance_id)
            elif chaos_type == 'instance_stop':
                return self.stop_instance(instance_id)
            elif chaos_type == 'network_latency':
                return self.introduce_network_latency(instance_id)
            elif chaos_type == 'cpu_stress':
                return self.stress_cpu(instance_id)
            elif chaos_type == 'memory_stress':
                return self.stress_memory(instance_id)
            elif chaos_type == 'disk_io_stress':
                return self.stress_disk_io(instance_id)
            else:
                return False, f"Unknown chaos type: {chaos_type}"
                
        except Exception as e:
            logger.error(f"Error executing chaos {chaos_type} on {instance_id}: {e}")
            return False, str(e)
    
    def terminate_instance(self, instance_id):
        """Terminate an EC2 instance."""
        try:
            ec2.terminate_instances(InstanceIds=[instance_id])
            logger.info(f"Terminated instance {instance_id}")
            return True, None
        except Exception as e:
            logger.error(f"Failed to terminate instance {instance_id}: {e}")
            return False, str(e)
    
    def stop_instance(self, instance_id):
        """Stop an EC2 instance."""
        try:
            ec2.stop_instances(InstanceIds=[instance_id])
            logger.info(f"Stopped instance {instance_id}")
            return True, None
        except Exception as e:
            logger.error(f"Failed to stop instance {instance_id}: {e}")
            return False, str(e)
    
    def introduce_network_latency(self, instance_id):
        """Introduce network latency using SSM."""
        try:
            command = '''
            #!/bin/bash
            # Introduce network latency
            tc qdisc add dev eth0 root netem delay 100ms 50ms distribution normal
            sleep 300
            tc qdisc del dev eth0 root
            '''
            
            response = ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': [command]}
            )
            
            logger.info(f"Introduced network latency on instance {instance_id}")
            return True, None
            
        except Exception as e:
            logger.error(f"Failed to introduce network latency on {instance_id}: {e}")
            return False, str(e)
    
    def stress_cpu(self, instance_id):
        """Stress CPU using SSM."""
        try:
            command = '''
            #!/bin/bash
            # Stress CPU for 5 minutes
            stress --cpu 4 --timeout 300s &
            sleep 300
            killall stress
            '''
            
            response = ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': [command]}
            )
            
            logger.info(f"Stressed CPU on instance {instance_id}")
            return True, None
            
        except Exception as e:
            logger.error(f"Failed to stress CPU on {instance_id}: {e}")
            return False, str(e)
    
    def stress_memory(self, instance_id):
        """Stress memory using SSM."""
        try:
            command = '''
            #!/bin/bash
            # Stress memory for 5 minutes
            stress --vm 2 --vm-bytes 1G --timeout 300s &
            sleep 300
            killall stress
            '''
            
            response = ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': [command]}
            )
            
            logger.info(f"Stressed memory on instance {instance_id}")
            return True, None
            
        except Exception as e:
            logger.error(f"Failed to stress memory on {instance_id}: {e}")
            return False, str(e)
    
    def stress_disk_io(self, instance_id):
        """Stress disk I/O using SSM."""
        try:
            command = '''
            #!/bin/bash
            # Stress disk I/O for 5 minutes
            stress --io 4 --timeout 300s &
            sleep 300
            killall stress
            '''
            
            response = ssm.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': [command]}
            )
            
            logger.info(f"Stressed disk I/O on instance {instance_id}")
            return True, None
            
        except Exception as e:
            logger.error(f"Failed to stress disk I/O on {instance_id}: {e}")
            return False, str(e)
    
    def log_chaos_event(self, instance_id, chaos_type, success, error_message=None):
        """Log the chaos event to CloudWatch Logs."""
        try:
            log_message = {
                'timestamp': datetime.utcnow().isoformat(),
                'event_type': 'chaos_monkey_event',
                'instance_id': instance_id,
                'chaos_type': chaos_type,
                'chaos_level': self.chaos_level,
                'dry_run': self.dry_run,
                'success': success,
                'error_message': error_message,
                'duration': 300  # 5 minutes default
            }
            
            # This would normally call the logging lambda, but for simplicity
            # we'll just log to CloudWatch directly
            logger.info(f"Chaos event: {json.dumps(log_message)}")
            
        except Exception as e:
            logger.error(f"Error logging chaos event: {e}")


def handler(event, context):
    """Lambda handler for chaos monkey."""
    try:
        logger.info(f"Chaos Monkey triggered with event: {json.dumps(event)}")
        
        monkey = ChaosMonkey()
        
        # Check if we should trigger chaos
        if not monkey.should_trigger_chaos():
            logger.info("Chaos probability not met, skipping this run")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No chaos triggered this time'})
            }
        
        # Get target instances
        target_instances = monkey.get_target_instances()
        
        if not target_instances:
            logger.info("No target instances available or below minimum count")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No target instances available'})
            }
        
        # Select a random target instance
        target_instance = random.choice(target_instances)
        
        # Select chaos type
        chaos_type = monkey.select_chaos_type()
        
        # Execute chaos
        success, error_message = monkey.execute_chaos(target_instance, chaos_type)
        
        # Log the event
        monkey.log_chaos_event(target_instance, chaos_type, success, error_message)
        
        # Return result
        if success:
            logger.info(f"Chaos successfully executed on {target_instance}")
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': f'Chaos executed successfully',
                    'instance_id': target_instance,
                    'chaos_type': chaos_type,
                    'chaos_level': monkey.chaos_level,
                    'dry_run': monkey.dry_run
                })
            }
        else:
            logger.error(f"Chaos failed on {target_instance}: {error_message}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': f'Chaos execution failed: {error_message}',
                    'instance_id': target_instance,
                    'chaos_type': chaos_type
                })
            }
            
    except Exception as e:
        logger.error(f"Error in chaos monkey handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Handler error: {str(e)}'})
        }


# Test function for local testing
if __name__ == "__main__":
    # Mock environment variables for testing
    os.environ['CHAOS_LEVEL'] = 'gentle'
    os.environ['DRY_RUN'] = 'true'
    os.environ['MIN_INSTANCE_COUNT'] = '1'
    
    test_event = {
        'source': 'aws.events',
        'detail-type': 'Scheduled Event',
        'time': datetime.utcnow().isoformat()
    }
    
    result = handler(test_event, None)
    print(f"Test result: {result}")
