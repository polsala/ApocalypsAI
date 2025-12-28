import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chaos_lambda import lambda_handler


class TestOutputs(unittest.TestCase):
    """Test output validation and structure"""
    
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
        'CHAOS_INTENSITY': '5',
        'TARGET_RESOURCES': '[]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_lambda_handler_output_structure(self, mock_ecs, mock_rds, mock_ec2):
        """Test that lambda handler returns correct output structure"""
        # Mock empty resource lists
        mock_ec2.return_value = []
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Check response structure
        self.assertIn('statusCode', result)
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('body', result)
        
        # Parse body
        body = json.loads(result['body'])
        
        # Check required fields
        self.assertIn('timestamp', body)
        self.assertIn('total_resources', body)
        self.assertIn('unprotected_resources', body)
        self.assertIn('selected_for_termination', body)
        self.assertIn('successful_terminations', body)
        self.assertIn('failed_terminations', body)
        self.assertIn('chaos_events', body)
        
        # Check data types
        self.assertIsInstance(body['timestamp'], str)
        self.assertIsInstance(body['total_resources'], int)
        self.assertIsInstance(body['unprotected_resources'], int)
        self.assertIsInstance(body['selected_for_termination'], int)
        self.assertIsInstance(body['successful_terminations'], int)
        self.assertIsInstance(body['failed_terminations'], int)
        self.assertIsInstance(body['chaos_events'], list)
    
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
    def test_lambda_handler_output_with_resources(self, mock_ecs, mock_rds, mock_ec2):
        """Test lambda handler output when resources are present"""
        # Mock EC2 instances
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
        
        # Parse body
        body = json.loads(result['body'])
        
        # Check that resources were found
        self.assertEqual(body['total_resources'], 1)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)
        
        # Check chaos events structure
        self.assertEqual(len(body['chaos_events']), 1)
        event = body['chaos_events'][0]
        
        self.assertIn('timestamp', event)
        self.assertIn('resource_id', event)
        self.assertIn('resource_type', event)
        self.assertIn('resource_name', event)
        self.assertIn('action', event)
        self.assertIn('success', event)
        
        self.assertEqual(event['resource_id'], 'i-1234567890abcdef0')
        self.assertEqual(event['resource_type'], 'aws_instance')
        self.assertEqual(event['resource_name'], 'test-instance')
        self.assertEqual(event['action'], 'terminate')
        self.assertTrue(event['success'])  # Should succeed in safe mode
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '0',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_lambda_handler_output_zero_intensity(self, mock_ecs, mock_rds, mock_ec2):
        """Test lambda handler output with zero chaos intensity"""
        # Mock EC2 instances
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
        
        # Parse body
        body = json.loads(result['body'])
        
        # Check that no resources were selected for termination
        self.assertEqual(body['total_resources'], 1)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)  # Minimum 1
        
        # Check chaos events
        self.assertEqual(len(body['chaos_events']), 1)
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '50',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'false',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    @patch('src.chaos_lambda.terminate_ec2_instance')
    def test_lambda_handler_output_actual_termination(self, mock_terminate, mock_ecs, mock_rds, mock_ec2):
        """Test lambda handler output when actual termination occurs"""
        # Mock EC2 instances
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
        mock_terminate.return_value = True
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse body
        body = json.loads(result['body'])
        
        # Check that termination was attempted
        self.assertEqual(body['total_resources'], 1)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)
        self.assertEqual(body['successful_terminations'], 1)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Check chaos events
        self.assertEqual(len(body['chaos_events']), 1)
        event = body['chaos_events'][0]
        self.assertTrue(event['success'])
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '50',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'false',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    @patch('src.chaos_lambda.terminate_ec2_instance')
    def test_lambda_handler_output_termination_failure(self, mock_terminate, mock_ecs, mock_rds, mock_ec2):
        """Test lambda handler output when termination fails"""
        # Mock EC2 instances
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
        
        # Parse body
        body = json.loads(result['body'])
        
        # Check that termination was attempted but failed
        self.assertEqual(body['total_resources'], 1)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)
        self.assertEqual(body['successful_terminations'], 0)
        self.assertEqual(body['failed_terminations'], 1)
        
        # Check chaos events
        self.assertEqual(len(body['chaos_events']), 1)
        event = body['chaos_events'][0]
        self.assertFalse(event['success'])
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '5',
        'TARGET_RESOURCES': '["aws_instance", "aws_rds_instance", "aws_ecs_service"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_lambda_handler_output_multiple_resource_types(self, mock_ecs, mock_rds, mock_ec2):
        """Test lambda handler output with multiple resource types"""
        # Mock multiple resource types
        mock_ec2.return_value = [
            {
                'id': 'i-1234567890abcdef0',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': 'test-ec2'}],
                'name': 'test-ec2'
            }
        ]
        mock_rds.return_value = [
            {
                'id': 'test-rds-instance',
                'type': 'aws_rds_instance',
                'state': 'available',
                'tags': [{'Key': 'Name', 'Value': 'test-rds'}],
                'name': 'test-rds'
            }
        ]
        mock_ecs.return_value = [
            {
                'id': 'test-ecs-service',
                'type': 'aws_ecs_service',
                'state': 'ACTIVE',
                'tags': [{'Key': 'Name', 'Value': 'test-ecs'}],
                'name': 'test-ecs',
                'clusterArn': 'arn:aws:ecs:us-east-1:123456789012:cluster/test-cluster'
            }
        ]
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse body
        body = json.loads(result['body'])
        
        # Check that all resource types were found
        self.assertEqual(body['total_resources'], 3)
        self.assertEqual(body['unprotected_resources'], 3)
        self.assertEqual(body['selected_for_termination'], 1)  # 5% of 3 = 0.15, minimum 1
        
        # Check chaos events
        self.assertEqual(len(body['chaos_events']), 1)
        event = body['chaos_events'][0]
        self.assertIn(event['resource_type'], ['aws_instance', 'aws_rds_instance', 'aws_ecs_service'])
        self.assertTrue(event['success'])


if __name__ == '__main__':
    unittest.main()
