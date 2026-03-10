import os
import json
import logging
from datetime import datetime

# Configure logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'temporal-anomaly-default-bucket')

def lambda_handler(event, context):
    """
    Handles incoming temporal anomaly events.
    Logs the event and returns a whimsical message.
    """
    current_time = datetime.utcnow().isoformat() + "Z"
    request_id = context.aws_request_id if context else "unknown-request-id"

    logger.info(f"[{current_time}] Temporal Anomaly Beacon activated! Request ID: {request_id}")
    logger.debug(f"Received event: {json.dumps(event)}")

    # In a real scenario, you might process the event, store data in S3, etc.
    # For now, we just log and return a whimsical message.
    anomaly_data = {
        "timestamp": current_time,
        "message": "A ripple in the fabric of spacetime detected!",
        "event_details": event,
        "s3_target_bucket": S3_BUCKET_NAME
    }

    logger.info(f"Anomaly data prepared: {json.dumps(anomaly_data)}")

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Temporal anomaly logged. Keep calm and carry chronometers!',
            'beacon_status': 'Active',
            'processed_at': current_time
        })
    }
