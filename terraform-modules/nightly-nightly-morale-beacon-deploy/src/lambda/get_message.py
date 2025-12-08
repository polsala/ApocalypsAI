import json
import os
import random

def lambda_handler(event, context):
    """
    AWS Lambda handler to return a random uplifting message.
    Messages are loaded from the UPLIFTING_MESSAGES environment variable.
    """
    try:
        messages_str = os.environ.get('UPLIFTING_MESSAGES', '["Keep going!", "You got this!"]')
        messages = json.loads(messages_str)

        if not messages:
            messages = ["No messages configured, but keep your spirits high!"]

        message = random.choice(messages)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*', # Allow CORS for web clients
            },
            'body': json.dumps({'message': message})
        }
    except Exception as e:
        print(f"Error processing request: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Failed to retrieve message', 'details': str(e)})
        }

if __name__ == '__main__':
    # Example local invocation for testing
    os.environ['UPLIFTING_MESSAGES'] = json.dumps([
        "Local test message 1",
        "Local test message 2",
        "Local test message 3"
    ])
    response = lambda_handler({}, {})
    print(json.loads(response['body'])['message'])
