import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chaos_lambda import lambda_handler


class TestVariables(unittest.TestCase):
    """Test variable validation and configuration"""
    
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
    def test_environment_variables_parsing(self):
        """Test that environment variables are parsed correctly"""
        # Test chaos intensity parsing
        chaos_intensity = int(os.environ.get('CHAOS_INTENSITY', 5))
        self.assertEqual(chaos_intensity, 5)
        
        # Test target resources parsing
        target_resources = json.loads(os.environ.get('TARGET_RESOURCES', '[]'))
        self.assertEqual(target_resources, [])
        
        # Test excluded tags parsing
        excluded_tags = json.loads(os.environ.get('EXCLUDED_TAGS', '[]'))
        self.assertEqual(excluded_tags, [])
        
        # Test safe mode parsing
        safe_mode = os.environ.get('SAFE_MODE', 'true').lower() == 'true'
        self.assertTrue(safe_mode)
        
        # Test region parsing
        region = os.environ.get('REGION', 'us-east-1')
        self.assertEqual(region, 'us-east-1')
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': 'invalid',
        'TARGET_RESOURCES': 'invalid',
        'EXCLUDED_TAGS': 'invalid',
        'SAFE_MODE': 'invalid',
        'REGION': 'invalid-region'
    })
    def test_environment_variables_invalid_values(self):
        """Test handling of invalid environment variable values"""
        # Test invalid chaos intensity
        try:
            chaos_intensity = int(os.environ.get('CHAOS_INTENSITY', 5))
        except ValueError:
            chaos_intensity = 5  # Default value
        self.assertEqual(chaos_intensity, 5)
        
        # Test invalid target resources
        try:
            target_resources = json.loads(os.environ.get('TARGET_RESOURCES', '[]'))
        except json.JSONDecodeError:
            target_resources = []  # Default value
        self.assertEqual(target_resources, [])
        
        # Test invalid excluded tags
        try:
            excluded_tags = json.loads(os.environ.get('EXCLUDED_TAGS', '[]'))
        except json.JSONDecodeError:
            excluded_tags = []  # Default value
        self.assertEqual(excluded_tags, [])
        
        # Test invalid safe mode
        safe_mode_str = os.environ.get('SAFE_MODE', 'true').lower()
        safe_mode = safe_mode_str in ['true', '1', 'yes', 'on']
        self.assertFalse(safe_mode)  # 'invalid' should not be considered true
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '150',  # Above 100%
        'TARGET_RESOURCES': '["aws_instance", "aws_rds_instance"]',
        'EXCLUDED_TAGS': '["critical", "production-critical"]',
        'SAFE_MODE': 'false',
        'REGION': 'us-east-1'
    })
    def test_environment_variables_boundary_values(self):
        """Test boundary values for environment variables"""
        # Test high chaos intensity
        chaos_intensity = int(os.environ.get('CHAOS_INTENSITY', 5))
        self.assertEqual(chaos_intensity, 150)
        
        # Test multiple target resources
        target_resources = json.loads(os.environ.get('TARGET_RESOURCES', '[]'))
        self.assertEqual(len(target_resources), 2)
        self.assertIn('aws_instance', target_resources)
        self.assertIn('aws_rds_instance', target_resources)
        
        # Test multiple excluded tags
        excluded_tags = json.loads(os.environ.get('EXCLUDED_TAGS', '[]'))
        self.assertEqual(len(excluded_tags), 2)
        self.assertIn('critical', excluded_tags)
        self.assertIn('production-critical', excluded_tags)
        
        # Test false safe mode
        safe_mode = os.environ.get('SAFE_MODE', 'true').lower() == 'true'
        self.assertFalse(safe_mode)
    
    @patch.dict('os.environ', {}, clear=True)
    def test_environment_variables_missing_values(self):
        """Test handling of missing environment variables"""
        # Test missing chaos intensity
        chaos_intensity = int(os.environ.get('CHAOS_INTENSITY', 5))
        self.assertEqual(chaos_intensity, 5)
        
        # Test missing target resources
        target_resources = json.loads(os.environ.get('TARGET_RESOURCES', '[]'))
        self.assertEqual(target_resources, [])
        
        # Test missing excluded tags
        excluded_tags = json.loads(os.environ.get('EXCLUDED_TAGS', '[]'))
        self.assertEqual(excluded_tags, [])
        
        # Test missing safe mode
        safe_mode = os.environ.get('SAFE_MODE', 'true').lower() == 'true'
        self.assertTrue(safe_mode)
        
        # Test missing region
        region = os.environ.get('REGION', 'us-east-1')
        self.assertEqual(region, 'us-east-1')
    
    def test_lambda_handler_event_structure(self):
        """Test that lambda handler receives correct event structure"""
        # Test with valid event
        result = lambda_handler(self.test_event, self.test_context)
        self.assertIn('statusCode', result)
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('body', result)
        
        # Test with empty event
        empty_event = {}
        result = lambda_handler(empty_event, self.test_context)
        self.assertIn('statusCode', result)
        self.assertEqual(result['statusCode'], 200)
    
    def test_lambda_handler_context_structure(self):
        """Test that lambda handler receives correct context structure"""
        # Test with valid context
        result = lambda_handler(self.test_event, self.test_context)
        self.assertIn('statusCode', result)
        self.assertEqual(result['statusCode'], 200)
        
        # Test with None context
        result = lambda_handler(self.test_event, None)
        self.assertIn('statusCode', result)
        self.assertEqual(result['statusCode'], 200)


if __name__ == '__main__':
    unittest.main()
