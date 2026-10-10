import json
import os
import datetime
import boto3

s3 = boto3.client('s3')
bucket_name = os.environ.get('BUCKET_NAME')

def handler(event, context):
    """
    Handles incoming API Gateway requests for the Temporal Echo Chamber.
    - POST /echo: Stores a new message (echo) with a timestamp.
    - GET /echo: Retrieves echoes, optionally filtered by a timestamp prefix.
    """
    if not bucket_name:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'BUCKET_NAME environment variable not set.'})
        }

    http_method = event.get('httpMethod')
    path = event.get('path')

    if http_method == 'POST' and path == '/echo':
        try:
            body = json.loads(event.get('body', '{}'))
            message = body.get('message')
            if not message:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Message not provided in request body.'})
                }

            timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+', 'Z').replace(':', '-')
            key = f"echoes/{timestamp}.txt" # Store as text file
            s3.put_object(Bucket=bucket_name, Key=key, Body=message.encode('utf-8'))

            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'status': 'echo received', 'timestamp': timestamp})
            }
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON in request body.'})
            }
        except Exception as e:
            print(f"Error processing POST request: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Failed to store echo: {str(e)}'})
            }

    elif http_method == 'GET' and path == '/echo':
        try:
            query_params = event.get('queryStringParameters', {})
            prefix = query_params.get('prefix', 'echoes/') # e.g., 'echoes/2023-10-27'
            max_echoes = int(query_params.get('limit', 10)) # Limit number of echoes returned

            response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            echo_keys = sorted([obj['Key'] for obj in response.get('Contents', [])], reverse=True)[:max_echoes]

            echoes = []
            for key in echo_keys:
                obj = s3.get_object(Bucket=bucket_name, Key=key)
                body = obj['Body'].read().decode('utf-8')
                echoes.append({'key': key, 'message': body})

            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'echoes': echoes})
            }
        except Exception as e:
            print(f"Error processing GET request: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Failed to retrieve echoes: {str(e)}'})
            }

    return {
        'statusCode': 404,
        'body': json.dumps({'error': 'Not Found or Unsupported Method/Path'})
    }
