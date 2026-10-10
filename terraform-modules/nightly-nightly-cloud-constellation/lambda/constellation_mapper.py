import os
import json
import datetime
# import boto3 # Uncomment and configure if running in a real AWS Lambda environment

def lambda_handler(event, context):
    """
    Scans for AWS resources and categorizes them into 'constellations'.
    In a real scenario, this would use boto3 to scan actual resources.
    """
    print(f"Cloud Constellation Mapper triggered at {datetime.datetime.now()}")
    print(f"Event: {json.dumps(event)}")

    # Mock data for demonstration. In a real scenario, boto3 would be used
    # to list resources (e.g., EC2, S3, RDS) and extract their tags.
    # Example: ec2_client = boto3.client('ec2', region_name=os.environ.get('AWS_REGION'))
    # instances = ec2_client.describe_instances()
    mock_resources = [
        {"name": "Stellar-API-Gateway", "type": "API Gateway", "tags": {"Project": "Orion", "Environment": "Production"}},
        {"name": "Nebula-DB-Cluster", "type": "RDS", "tags": {"Project": "Orion", "Environment": "Production"}},
        {"name": "Cosmic-Data-Lake", "type": "S3 Bucket", "tags": {"Project": "Andromeda", "Environment": "Development"}},
        {"name": "Rogue-Instance-X", "type": "EC2", "tags": {}}, # Untagged resource
        {"name": "Lost-Volume-Y", "type": "EBS Volume", "tags": {"Owner": "Unknown"}}, # Partially tagged
    ]

    constellations = {}
    rogue_stars = []

    project_tag_key = os.environ.get('PROJECT_TAG_KEY', 'Project')
    environment_tag_key = os.environ.get('ENVIRONMENT_TAG_KEY', 'Environment')
    s3_bucket_name = os.environ.get('S3_BUCKET_NAME')

    for resource in mock_resources:
        project = resource['tags'].get(project_tag_key, 'Unassigned Project')
        environment = resource['tags'].get(environment_tag_key, 'Unknown Environment')

        if not resource['tags'] or not resource['tags'].get(project_tag_key) or not resource['tags'].get(environment_tag_key):
            rogue_stars.append(resource)

        key = f"Project:{project}-Env:{environment}"
        if key not in constellations:
            constellations[key] = []
        constellations[key].append(resource)

    output_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "constellations": constellations,
        "rogue_stars": rogue_stars,
        "message": "Cloud Constellation Map generated!"
    }

    if s3_bucket_name:
        # In a real scenario, this would upload to an S3 bucket
        # s3 = boto3.client('s3')
        # s3_key = f"constellation-maps/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
        # s3.put_object(Bucket=s3_bucket_name, Key=s3_key, Body=json.dumps(output_data, indent=2))
        print(f"Mock: Constellation map would be uploaded to s3://{s3_bucket_name}/constellation-maps/...")
    else:
        print("S3_BUCKET_NAME not set in environment, printing map to console.")

    print(json.dumps(output_data, indent=2))
    return {
        'statusCode': 200,
        'body': json.dumps('Constellation mapping complete!')
    }

if __name__ == '__main__':
    # Example local execution
    os.environ['PROJECT_TAG_KEY'] = 'Project'
    os.environ['ENVIRONMENT_TAG_KEY'] = 'Environment'
    os.environ['S3_BUCKET_NAME'] = 'mock-s3-bucket'
    lambda_handler({}, {})
