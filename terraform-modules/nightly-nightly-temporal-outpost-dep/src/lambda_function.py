import os
import json
import datetime
import random
import boto3

def handler(event, context):
    s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
    if not s3_bucket_name:
        print("S3_BUCKET_NAME environment variable not set.")
        return {
            'statusCode': 500,
            'body': json.dumps('Configuration error: S3_BUCKET_NAME missing.')
        }

    s3 = boto3.client('s3')
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Whimsical temporal anomaly detection logic
    anomaly_chance = random.random()
    if anomaly_chance < 0.05: # 5% chance of a major anomaly
        status = "MAJOR TEMPORAL ANOMALY DETECTED! Reality is wobbly."
        severity = "CRITICAL"
    elif anomaly_chance < 0.20: # 15% chance of a minor ripple
        status = "Minor temporal ripple detected. Keep calm and carry on."
        severity = "WARNING"
    else:
        status = "Temporal signature stable. All clear for now."
        severity = "INFO"

    log_entry = {
        "timestamp": timestamp,
        "outpost_id": context.aws_request_id,
        "status": status,
        "severity": severity,
        "message": "ApocalypsAI Temporal Outpost heartbeat."
    }

    file_name = f"temporal-logs/{timestamp.split('T')[0]}/{context.aws_request_id}-{timestamp}.json"

    try:
        s3.put_object(
            Bucket=s3_bucket_name,
            Key=file_name,
            Body=json.dumps(log_entry, indent=2),
            ContentType='application/json'
        )
        print(f"Logged temporal signature to s3://{s3_bucket_name}/{file_name}")
        return {
            'statusCode': 200,
            'body': json.dumps(f'Temporal signature logged: {status}')
        }
    except Exception as e:
        print(f"Error logging to S3: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error logging temporal signature: {str(e)}')
        }
