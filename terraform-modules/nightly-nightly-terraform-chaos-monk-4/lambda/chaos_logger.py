import json
import boto3
import os
import logging
import time
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

cloudwatch = boto3.client('logs')

LOG_GROUP_NAME = os.environ.get('LOG_GROUP_NAME', '/apocalypsaid/chaos-monkey')
LOG_STREAM_NAME = os.environ.get('LOG_STREAM_NAME', 'chaos-events')


def get_sequence_token():
    """Get the sequence token for the log stream."""
    try:
        response = cloudwatch.describe_log_streams(
            logGroupName=LOG_GROUP_NAME,
            logStreamNamePrefix=LOG_STREAM_NAME
        )
        log_stream = next(
            (stream for stream in response['logStreams'] if stream['logStreamName'] == LOG_STREAM_NAME),
            None
        )
        return log_stream['uploadSequenceToken'] if log_stream else None
    except Exception as e:
        logger.warning(f"Could not get sequence token: {e}")
        return None


def put_log_event(message):
    """Put a log event to CloudWatch Logs."""
    try:
        sequence_token = get_sequence_token()
        
        log_event = {
            'timestamp': int(time.time() * 1000),
            'message': message
        }
        
        kwargs = {
            'logGroupName': LOG_GROUP_NAME,
            'logStreamName': LOG_STREAM_NAME,
            'logEvents': [log_event]
        }
        
        if sequence_token:
            kwargs['sequenceToken'] = sequence_token
        
        cloudwatch.put_log_events(**kwargs)
        return True
    except Exception as e:
        logger.error(f"Error putting log event: {e}")
        return False


def handler(event, context):
    """Lambda handler for chaos monkey events."""
    try:
        # Parse the event
        if isinstance(event, dict) and 'detail' in event:
            # EventBridge event
            chaos_event = event['detail']
        elif isinstance(event, dict):
            # Direct invocation
            chaos_event = event
        else:
            # SNS or other format
            chaos_event = json.loads(event.get('Message', '{}'))
        
        # Prepare log message
        log_message = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': 'chaos_monkey_event',
            'instance_id': chaos_event.get('instance_id', 'unknown'),
            'chaos_type': chaos_event.get('chaos_type', 'unknown'),
            'chaos_level': chaos_event.get('chaos_level', 'unknown'),
            'dry_run': chaos_event.get('dry_run', False),
            'target_type': chaos_event.get('target_type', 'unknown'),
            'region': chaos_event.get('region', 'unknown'),
            'duration': chaos_event.get('duration', 0),
            'success': chaos_event.get('success', True),
            'error_message': chaos_event.get('error_message', None)
        }
        
        # Add additional context if available
        if 'additional_info' in chaos_event:
            log_message['additional_info'] = chaos_event['additional_info']
        
        # Put log event
        success = put_log_event(json.dumps(log_message))
        
        if success:
            logger.info(f"Chaos event logged successfully: {log_message['instance_id']}")
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Chaos event logged successfully'})
            }
        else:
            logger.error("Failed to log chaos event")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to log chaos event'})
            }
            
    except Exception as e:
        logger.error(f"Error in chaos logger handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Handler error: {str(e)}'})
        }


# Test function for local testing
if __name__ == "__main__":
    test_event = {
        'instance_id': 'i-1234567890abcdef0',
        'chaos_type': 'instance_termination',
        'chaos_level': 'medium',
        'dry_run': True,
        'target_type': 'ec2',
        'region': 'us-east-1',
        'duration': 5,
        'success': True
    }
    
    result = handler(test_event, None)
    print(f"Test result: {result}")
