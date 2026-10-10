import json
import os
import time
import uuid
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('DYNAMODB_TABLE_NAME', 'ApocalypsAIWhispers')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    http_method = event.get('httpMethod')
    path = event.get('path')

    # CORS headers for static website access
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'CORS preflight successful'})
        }

    if http_method == 'POST' and path == '/whispers':
        return handle_post_whisper(event, headers)
    elif http_method == 'GET' and path == '/whispers':
        return handle_get_whispers(event, headers)
    else:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'message': 'Unsupported method or path'})
        }

def handle_post_whisper(event, headers):
    try:
        body = json.loads(event['body'])
        message = body.get('message')
        if not message or not isinstance(message, str) or len(message.strip()) == 0:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Message is required and must be a non-empty string.'})
            }
        
        # Trim message to prevent excessively long whispers
        message = message.strip()[:500] # Max 500 characters

        whisper_id = str(uuid.uuid4())
        timestamp = int(time.time())
        
        # Get TTL from environment variable, default to 24 hours (86400 seconds)
        whisper_ttl_seconds = int(os.environ.get('WHISPER_TTL_SECONDS', 86400))
        expiration_time = timestamp + whisper_ttl_seconds

        table.put_item(
            Item={
                'id': whisper_id,
                'message': message,
                'timestamp': timestamp,
                'expirationTime': expiration_time # DynamoDB TTL attribute
            }
        )

        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({'message': 'Whisper posted successfully', 'id': whisper_id})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'message': 'Invalid JSON body.'})
        }
    except ClientError as e:
        print(f"DynamoDB error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Failed to post whisper due to database error.'})
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'An unexpected error occurred.'})
        }

def handle_get_whispers(event, headers):
    try:
        # Scan is used for simplicity for a whimsical post. For large-scale production,
        # consider more efficient query patterns or pagination.
        response = table.scan()
        whispers = sorted(response.get('Items', []), key=lambda x: x.get('timestamp', 0), reverse=True)
        
        # Filter out expirationTime from output for cleaner display
        for whisper in whispers:
            whisper.pop('expirationTime', None)

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'whispers': whispers})
        }
    except ClientError as e:
        print(f"DynamoDB error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Failed to retrieve whispers due to database error.'})
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'An unexpected error occurred.'})
        }
