import json
import os

def lambda_handler(event, context):
    """
    Reflects the incoming 'starlight signal' (HTTP request body) back.
    """
    print(f"Received starlight signal event: {json.dumps(event)}")

    try:
        # Assuming API Gateway proxy integration
        body = event.get('body', '{}')
        if event.get('isBase64Encoded'):
            import base64
            body = base64.b64decode(body).decode('utf-8')

        # Attempt to parse body as JSON, otherwise treat as plain text
        try:
            parsed_body = json.loads(body)
            response_body = {
                "message": "Starlight signal reflected!",
                "received_signal": parsed_body
            }
        except json.JSONDecodeError:
            response_body = {
                "message": "Starlight signal reflected!",
                "received_signal": body
            }

        status_code = 200

    except Exception as e:
        print(f"Error processing starlight signal: {e}")
        status_code = 500
        response_body = {
            "message": "Failed to reflect starlight signal due to internal anomaly.",
            "error": str(e)
        }

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'X-Reflector-ID': os.environ.get('REFLECTOR_ID', 'UNKNOWN')
        },
        'body': json.dumps(response_body)
    }
