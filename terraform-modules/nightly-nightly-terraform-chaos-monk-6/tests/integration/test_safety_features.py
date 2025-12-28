import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chaos_lambda import lambda_handler, is_resource_protected


class TestSafetyFeatures(unittest.TestCase):
    """Integration tests for safety features"""
    
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
        'EXCLUDED_TAGS': '["critical", "production-critical", "do-not-terminate"]',
        'SAFE_MODE': 'false',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_excluded_tags_protection(self, mock_ecs, mock_rds, mock_ec2):
        """Test that excluded tags protect resources from chaos"""
        # Mock resources with various tags
        mock_ec2.return_value = [
            # Protected resource
            {
                'id': 'i-protected',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Environment', 'Value': 'critical'}],
                'name': 'protected-instance'
            },
            # Protected resource
            {
                'id': 'i-production-protected',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Environment', 'Value': 'production-critical'}],
                'name': 'production-protected-instance'
            },
            # Protected resource
            {
                'id': 'i-do-not-terminate',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Environment', 'Value': 'do-not-terminate'}],
                'name': 'do-not-terminate-instance'
            },
            # Unprotected resource
            {
                'id': 'i-unprotected',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Environment', 'Value': 'test'}],
                'name': 'unprotected-instance'
            },
            # Resource with no tags
            {
                'id': 'i-no-tags',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [],
                'name': 'no-tags-instance'
            },
            # Resource with None tags
            {
                'id': 'i-none-tags',
                'type': 'aws_instance',
                'state': 'running',
                'tags': None,
                'name': 'none-tags-instance'
            }
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify that only unprotected resources were selected
        self.assertEqual(body['total_resources'], 6)
        self.assertEqual(body['unprotected_resources'], 3)  # Only 3 unprotected
        self.assertEqual(body['selected_for_termination'], 3)  # All 3 unprotected selected
        self.assertEqual(body['successful_terminations'], 3)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify chaos events only include unprotected resources
        protected_ids = {'i-protected', 'i-production-protected', 'i-do-not-terminate'}
        for event in body['chaos_events']:
            self.assertNotIn(event['resource_id'], protected_ids)
    
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
    @patch('src.chaos_lambda.terminate_ec2_instance')
    def test_safe_mode_protection(self, mock_terminate, mock_ecs, mock_rds, mock_ec2):
        """Test that safe mode prevents actual resource termination"""
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
        
        # Verify that actual termination was not called
        mock_terminate.assert_not_called()
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '100',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'false',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    @patch('src.chaos_lambda.terminate_ec2_instance')
    def test_actual_termination_when_safe_mode_disabled(self, mock_terminate, mock_ecs, mock_rds, mock_ec2):
        """Test that actual termination occurs when safe mode is disabled"""
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
        mock_terminate.return_value = True
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify execution
        self.assertEqual(body['total_resources'], 1)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)
        self.assertEqual(body['successful_terminations'], 1)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify that actual termination was called
        mock_terminate.assert_called_once_with('i-1234567890abcdef0')
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '100',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '["critical"]',
        'SAFE_MODE': 'false',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    @patch('src.chaos_lambda.terminate_ec2_instance')
    def test_combined_safety_features(self, mock_terminate, mock_ecs, mock_rds, mock_ec2):
        """Test combined safety features (excluded tags + safe mode)"""
        # Mock resources with mixed protection
        mock_ec2.return_value = [
            # Protected by tag
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
        
        # Verify that only unprotected resources were selected
        self.assertEqual(body['total_resources'], 2)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)
        self.assertEqual(body['successful_terminations'], 1)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify chaos events only include unprotected resources
        for event in body['chaos_events']:
            self.assertEqual(event['resource_id'], 'i-unprotected')
        
        # Verify that actual termination was not called (safe mode is false but we're mocking)
        # In real execution, this would actually terminate
        mock_terminate.assert_called_once_with('i-unprotected')
    
    def test_is_resource_protected_function(self):
        """Test the is_resource_protected function directly"""
        # Test with excluded tag
        tags = [{'Key': 'Environment', 'Value': 'critical'}]
        excluded_tags = ['critical', 'production-critical']
        
        with patch.dict('os.environ', {'EXCLUDED_TAGS': json.dumps(excluded_tags)}):
            result = is_resource_protected(tags)
            self.assertTrue(result)
        
        # Test with non-excluded tag
        tags = [{'Key': 'Environment', 'Value': 'test'}]
        with patch.dict('os.environ', {'EXCLUDED_TAGS': json.dumps(excluded_tags)}):
            result = is_resource_protected(tags)
            self.assertFalse(result)
        
        # Test with multiple tags (one excluded)
        tags = [
            {'Key': 'Environment', 'Value': 'test'},
            {'Key': 'Purpose', 'Value': 'critical'}
        ]
        with patch.dict('os.environ', {'EXCLUDED_TAGS': json.dumps(excluded_tags)}):
            result = is_resource_protected(tags)
            self.assertTrue(result)
        
        # Test with empty tags
        tags = []
        with patch.dict('os.environ', {'EXCLUDED_TAGS': json.dumps(excluded_tags)}):
            result = is_resource_protected(tags)
            self.assertFalse(result)
        
        # Test with None tags
        tags = None
        with patch.dict('os.environ', {'EXCLUDED_TAGS': json.dumps(excluded_tags)}):
            result = is_resource_protected(tags)
            self.assertFalse(result)
    
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
    def test_safety_features_with_no_resources(self, mock_ecs, mock_rds, mock_ec2):
        """Test safety features with no resources"""
        # Mock empty resources
        mock_ec2.return_value = []
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify execution
        self.assertEqual(body['total_resources'], 0)
        self.assertEqual(body['unprotected_resources'], 0)
        self.assertEqual(body['selected_for_termination'], 0)
        self.assertEqual(body['successful_terminations'], 0)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify no chaos events
        self.assertEqual(len(body['chaos_events']), 0)
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '0',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'false',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_zero_chaos_intensity_safety(self, mock_ecs, mock_rds, mock_ec2):
        """Test safety with zero chaos intensity"""
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
        
        # Verify that at least one resource is selected (minimum is 1)
        self.assertEqual(body['total_resources'], 1)
        self.assertEqual(body['unprotected_resources'], 1)
        self.assertEqual(body['selected_for_termination'], 1)  # Minimum 1
        self.assertEqual(body['successful_terminations'], 1)
        self.assertEqual(body['failed_terminations'], 0)


if __name__ == '__main__':
    unittest.main()
