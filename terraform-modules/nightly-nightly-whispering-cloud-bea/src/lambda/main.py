import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO'))

def handler(event, context):
    """
    AWS Lambda handler for the Whispering Cloud Beacon.
    Receives and logs incoming 'whispers' (messages).
    """
    logger.info("Received a whisper!")
    logger.debug(f"Event: {json.dumps(event)}")

    try:
        # Assuming a POST request with JSON body
        if 'body' in event and event['body']:
            body = json.loads(event['body'])
            message = body.get('message', 'No message provided.')
            logger.info(f"Whisper content: {message}")
            response_message = f"Whisper received: '{message}'"
        else:
            logger.info("No specific message in whisper body.")
            response_message = "Whisper received (no specific message)."

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'status': 'success', 'message': response_message})
        }
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body.")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'status': 'error', 'message': 'Invalid JSON format.'})
        }
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'status': 'error', 'message': 'Internal server error.'})
        }
