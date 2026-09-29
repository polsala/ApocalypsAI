import os
import boto3
import json

def lambda_handler(event, context):
    """
    AWS Lambda function to stop or start EC2 instances based on tags and a CloudWatch Event.
    """
    region = os.environ.get('REGION')
    resource_tags_str = os.environ.get('RESOURCE_TAGS')

    if not region or not resource_tags_str:
        print("Error: REGION or RESOURCE_TAGS environment variables not set.")
        return {'statusCode': 500, 'body': json.dumps("Missing environment variables.")}

    try:
        resource_tags = json.loads(resource_tags_str)
    except json.JSONDecodeError:
        print(f"Error: Could not parse RESOURCE_TAGS: {resource_tags_str}")
        return {'statusCode': 500, 'body': json.dumps("Invalid RESOURCE_TAGS format.")}

    # The action ('stop' or 'start') is passed in the CloudWatch event input
    action = event.get('detail', {}).get('action')
    if action not in ['stop', 'start']:
        print(f"Error: Invalid action specified in event: {action}")
        return {'statusCode': 400, 'body': json.dumps("Invalid action.")}

    ec2 = boto3.client('ec2', region_name=region)

    filters = []
    for key, value in resource_tags.items():
        filters.append({'Name': f'tag:{key}', 'Values': [value]})

    # Filter instances based on their current state for the intended action
    if action == 'stop':
        filters.append({'Name': 'instance-state-name', 'Values': ['running']})
    elif action == 'start':
        filters.append({'Name': 'instance-state-name', 'Values': ['stopped']})

    instances_to_process = []
    try:
        response = ec2.describe_instances(Filters=filters)
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances_to_process.append(instance['InstanceId'])
    except Exception as e:
        print(f"Error describing instances: {e}")
        return {'statusCode': 500, 'body': json.dumps(f"Error describing instances: {e}")}

    if not instances_to_process:
        print(f"No instances found to {action} with tags {resource_tags} in region {region}.")
        return {'statusCode': 200, 'body': json.dumps(f"No instances found to {action}.")}

    print(f"Found {len(instances_to_process)} instances to {action}: {instances_to_process}")

    try:
        if action == 'stop':
            ec2.stop_instances(InstanceIds=instances_to_process)
            print(f"Successfully initiated stop for instances: {instances_to_process}")
        elif action == 'start':
            ec2.start_instances(InstanceIds=instances_to_process)
            print(f"Successfully initiated start for instances: {instances_to_process}")
        return {'statusCode': 200, 'body': json.dumps(f"Successfully initiated {action} for instances.")}
    except Exception as e:
        print(f"Error {action}ing instances: {e}")
        return {'statusCode': 500, 'body': json.dumps(f"Error {action}ing instances: {e}")}
