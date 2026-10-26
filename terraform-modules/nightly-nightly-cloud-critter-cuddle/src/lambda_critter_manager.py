import os
import json
import boto3

ec2 = boto3.client('ec2')

def handler(event, context):
    instance_id = os.environ.get('INSTANCE_ID')
    action = event.get('action')

    if not instance_id or not action:
        print("Missing INSTANCE_ID environment variable or 'action' in event.")
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required parameters.')
        }

    try:
        if action == 'stop':
            print(f"Stopping instance: {instance_id}")
            ec2.stop_instances(InstanceIds=[instance_id])
            message = f"Instance {instance_id} stopped successfully."
        elif action == 'start':
            print(f"Starting instance: {instance_id}")
            ec2.start_instances(InstanceIds=[instance_id])
            message = f"Instance {instance_id} started successfully."
        else:
            message = f"Invalid action: {action}"
            print(message)
            return {
                'statusCode': 400,
                'body': json.dumps(message)
            }
        
        print(message)
        return {
            'statusCode': 200,
            'body': json.dumps(message)
        }
    except Exception as e:
        print(f"Error performing action {action} on instance {instance_id}: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
