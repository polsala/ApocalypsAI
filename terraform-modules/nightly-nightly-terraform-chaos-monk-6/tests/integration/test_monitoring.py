import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os
from datetime import datetime

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chaos_lambda import lambda_handler


class TestMonitoring(unittest.TestCase):
    """Integration tests for monitoring features"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_event = {
            'Records': [
                {
                    'eventVersion': '2.1',
                    'eventSource': 'aws:s3',
                    'awsRegion': 'us-east-1',
                    'eventTime': '2023-01-01T00:00:00.000Z',
                    'eventName': 'ObjectCreated:Put',
                    'userIdentity': {'principalId': 'test'},
                    'requestParameters': {'sourceIPAddress': '127.0.0.1'},
                    'responseElements': {
                        'x-amz-request-id': 'test',
                        'x-amz-id-2': 'test'
                    },
                    's3': {
                        's3SchemaVersion': '1.0',
                        'configurationId': 'test',
                        'bucket': {
                            'name': 'test-bucket',
                            'ownerIdentity': {'principalId': 'test'},
                            'arn': 'arn:aws:s3:::test-bucket'
                        },
                        'object': {
                            'key': 'test-key',
                            'size': 1024,
                            'eTag': 'test',
                            'sequencer': 'test'
                        }
                    }
                }
            ]
        }
        
        self.test_context = MagicMock()
        self.test_context.function_name = 'test-function'
        self.test_context.invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:test-function'
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '100',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1',
        'SNS_TOPIC_ARN': 'arn:aws:sns:us-east-1:123456789012:test-topic'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    @patch('src.chaos_lambda.boto3.client')
    def test_sns_notification_integration(self, mock_boto3_client, mock_ecs, mock_rds, mock_ec2):
        """Test SNS notification integration"""
        # Mock SNS client
        mock_sns = MagicMock()
        mock_boto3_client.return_value = mock_sns
        
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': 'i-1234567890abcdef0',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': 'test-instance'}],
                'name': 'test-instance'
            }
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify execution
        self.assertEqual(body['total_resources'], 1)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)
        self.assertEqual(body['successful_terminations'], 1)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify SNS notification was called
        mock_sns.publish.assert_called_once()
        call_args = mock_sns.publish.call_args
        self.assertEqual(call_args[1]['TopicArn'], 'arn:aws:sns:us-east-1:123456789012:test-topic')
        self.assertIn('Chaos Monkey Execution Report', call_args[1]['Subject'])
        self.assertIn('test-instance', call_args[1]['Message'])
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '100',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'false',
        'REGION': 'us-east-1',
        'SNS_TOPIC_ARN': 'arn:aws:sns:us-east-1:123456789012:test-topic'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    @patch('src.chaos_lambda.boto3.client')
    @patch('src.chaos_lambda.terminate_ec2_instance')
    def test_sns_notification_on_failure(self, mock_terminate, mock_boto3_client, mock_ecs, mock_rds, mock_ec2):
        """Test SNS notification on execution failure"""
        # Mock SNS client
        mock_sns = MagicMock()
        mock_boto3_client.return_value = mock_sns
        
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': 'i-1234567890abcdef0',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': 'test-instance'}],
                'name': 'test-instance'
            }
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        mock_terminate.return_value = False
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify execution
        self.assertEqual(body['total_resources'], 1)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)
        self.assertEqual(body['successful_terminations'], 0)
        self.assertEqual(body['failed_terminations'], 1)
        
        # Verify SNS notification was called
        mock_sns.publish.assert_called_once()
        call_args = mock_sns.publish.call_args
        self.assertEqual(call_args[1]['TopicArn'], 'arn:aws:sns:us-east-1:123456789012:test-topic')
        self.assertIn('Chaos Monkey Execution Report', call_args[1]['Subject'])
        self.assertIn('FAILURE', call_args[1]['Message'])
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '100',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_execution_timestamp_accuracy(self, mock_ecs, mock_rds, mock_ec2):
        """Test that execution timestamps are accurate"""
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': 'i-1234567890abcdef0',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': 'test-instance'}],
                'name': 'test-instance'
            }
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        # Record start time
        start_time = datetime.now()
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Record end time
        end_time = datetime.now()
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify execution timestamp is within reasonable range
        execution_time = datetime.fromisoformat(body['timestamp'].replace('Z', '+00:00'))
        self.assertGreaterEqual(execution_time, start_time)
        self.assertLessEqual(execution_time, end_time)
        
        # Verify chaos event timestamps
        for event in body['chaos_events']:
            event_time = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
            self.assertGreaterEqual(event_time, start_time)
            self.assertLessEqual(event_time, end_time)
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '100',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_chaos_event_details_completeness(self, mock_ecs, mock_rds, mock_ec2):
        """Test that chaos event details are complete"""
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': 'i-1234567890abcdef0',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': 'test-instance'}, {'Key': 'Environment', 'Value': 'test'}],
                'name': 'test-instance'
            }
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify chaos event details
        self.assertEqual(len(body['chaos_events']), 1)
        event = body['chaos_events'][0]
        
        # Check all required fields
        required_fields = ['timestamp', 'resource_id', 'resource_type', 'resource_name', 'action', 'success']
        for field in required_fields:
            self.assertIn(field, event, f"Missing field: {field}")
        
        # Check field values
        self.assertEqual(event['resource_id'], 'i-1234567890abcdef0')
        self.assertEqual(event['resource_type'], 'aws_instance')
        self.assertEqual(event['resource_name'], 'test-instance')
        self.assertEqual(event['action'], 'terminate')
        self.assertTrue(event['success'])
        
        # Check timestamp format
        try:
            datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
        except ValueError:
            self.fail("Invalid timestamp format")
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '100',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_chaos_execution_summary_accuracy(self, mock_ecs, mock_rds, mock_ec2):
        """Test that chaos execution summary is accurate"""
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': 'i-1',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': 'test-1'}],
                'name': 'test-1'
            },
            {
                'id': 'i-2',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': 'test-2'}],
                'name': 'test-2'
            }
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify summary accuracy
        self.assertEqual(body['total_resources'], 2)
        self.assertEqual(body['unprotected_resources'], 2)
        self.assertEqual(body['selected_for_termination'], 2)
        self.assertEqual(body['successful_terminations'], 2)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify summary math
        self.assertEqual(body['total_resources'], body['unprotected_resources'] + 0)  # No protected resources
        self.assertEqual(body['successful_terminations'] + body['failed_terminations'], body['selected_for_termination'])
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '50',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_chaos_execution_summary_partial_selection(self, mock_ecs, mock_rds, mock_ec2):
        """Test chaos execution summary with partial resource selection"""
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': f'i-{i}',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': f'test-{i}'}],
                'name': f'test-{i}'
            } for i in range(10)
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify summary accuracy
        self.assertEqual(body['total_resources'], 10)
        self.assertEqual(body['unprotected_resources'], 10)
        self.assertEqual(body['selected_for_termination'], 5)  # 50% of 10
        self.assertEqual(body['successful_terminations'], 5)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify summary math
        self.assertEqual(body['successful_terminations'] + body['failed_terminations'], body['selected_for_termination'])
        self.assertLess(body['selected_for_termination'], body['total_resources'])
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '100',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '["critical"]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_chaos_execution_summary_with_protection(self, mock_ecs, mock_rds, mock_ec2):
        """Test chaos execution summary with resource protection"""
        # Mock resources with protection
        mock_ec2.return_value = [
            # Protected
            {
                'id': 'i-protected',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Environment', 'Value': 'critical'}],
                'name': 'protected-instance'
            },
            # Unprotected
            {
                'id': 'i-unprotected',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Environment', 'Value': 'test'}],
                'name': 'unprotected-instance'
            }
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify summary accuracy
        self.assertEqual(body['total_resources'], 2)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)
        self.assertEqual(body['successful_terminations'], 1)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify summary math
        self.assertEqual(body['total_resources'], body['unprotected_resources'] + 1)  # 1 protected
        self.assertEqual(body['successful_terminations'] + body['failed_terminations'], body['selected_for_termination'])


if __name__ == '__main__':
    unittest.main()
