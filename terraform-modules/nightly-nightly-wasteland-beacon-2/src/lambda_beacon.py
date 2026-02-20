import json
import os
import datetime

def handler(event, context):
    """
    AWS Lambda handler for the Wasteland Resource Beacon.
    Emits a simple status signal to CloudWatch Logs.
    """
    beacon_name = os.environ.get('BEACON_NAME', 'UnknownBeacon')
    current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()

    message = {
        "status": "Beacon Signal Emitted",
        "beacon_name": beacon_name,
        "timestamp": current_time,
        "message": f"The Wasteland Beacon '{beacon_name}' is active and sending its heartbeat."
    }

    print(json.dumps(message))

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }

# For local testing/debugging
if __name__ == '__main__':
    # Mock rationale: Simulating Lambda invocation locally without AWS environment.
    # This allows for basic function logic testing.
    os.environ['BEACON_NAME'] = 'LocalTestBeacon'
    print("--- Local Test Invocation ---")
    handler({}, {})
    print("--- End Local Test ---")
