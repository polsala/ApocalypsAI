import json

def handler(event, context):
    """
    AWS Lambda handler to simulate tucking in the cloud critter.
    Logs a message and returns a success response.
    """
    message = "Critter tucked in for the night!"
    print(message)
    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
