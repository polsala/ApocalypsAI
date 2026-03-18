import os
import json
import datetime

def handler(event, context):
    """
    AWS Lambda handler that logs a predefined message along with a timestamp.
    The message is retrieved from the BEACON_MESSAGE environment variable.
    """
    beacon_message = os.environ.get('BEACON_MESSAGE', 'Temporal Beacon: All systems nominal. Time continues.')
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log_entry = {
        "message": beacon_message,
        "timestamp": timestamp,
        "source": "ApocalypsAI Temporal Beacon",
        "lambda_request_id": context.aws_request_id
    }
    print(json.dumps(log_entry))
    return {
        'statusCode': 200,
        'body': json.dumps('Beacon emitted successfully!')
    }
