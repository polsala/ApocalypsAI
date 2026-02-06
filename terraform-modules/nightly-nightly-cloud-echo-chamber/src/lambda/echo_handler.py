import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(os.environ.get('LOG_LEVEL', 'INFO').upper())

def lambda_handler(event, context):
    """
    AWS Lambda function to process S3 object creation events
    and echo their metadata to CloudWatch Logs.
    """
    logger.info("Received S3 event: %s", json.dumps(event))

    records = event.get('Records', [])
    if not records:
        logger.warning("No records found in the S3 event.")
        return {
            'statusCode': 200,
            'body': json.dumps('No records processed.')
        }

    processed_objects = []
    for record in records:
        if 's3' in record:
            s3_info = record['s3']
            bucket_name = s3_info['bucket']['name']
            object_key = s3_info['object']['key']
            object_size = s3_info['object'].get('size', 'N/A')
            object_etag = s3_info['object'].get('eTag', 'N/A')
            event_name = record.get('eventName', 'N/A')
            event_time = record.get('eventTime', 'N/A')

            echo_message = {
                "event_name": event_name,
                "event_time": event_time,
                "bucket": bucket_name,
                "key": object_key,
                "size": object_size,
                "etag": object_etag,
                "source_ip": record.get('requestParameters', {}).get('sourceIPAddress', 'N/A')
            }
            logger.info("Echoing object metadata: %s", json.dumps(echo_message))
            processed_objects.append(echo_message)
        else:
            logger.warning("Record does not contain S3 information: %s", json.dumps(record))

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully echoed {len(processed_objects)} S3 object(s) metadata.')
    }
