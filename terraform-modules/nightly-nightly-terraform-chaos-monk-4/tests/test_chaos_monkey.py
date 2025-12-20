import unittest
import json
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add the lambda directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))

# Import the chaos monkey module
from lambda_function import ChaosMonkey


class TestChaosMonkey(unittest.TestCase):
    """Test cases for the ChaosMonkey class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variables
        os.environ['CHAOS_LEVEL'] = 'medium'
        os.environ['DRY_RUN'] = 'true'
        os.environ['MIN_INSTANCE_COUNT'] = '1'
        os.environ['EXCLUDED_TAGS'] = 'Critical,Database'
        os.environ['INCLUDED_TAGS'] = '{"Environment": "test", "Team": "platform"}'
        
        self.monkey = ChaosMonkey()
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove test environment variables
        for key in ['CHAOS_LEVEL', 'DRY_RUN', 'MIN_INSTANCE_COUNT', 'EXCLUDED_TAGS', 'INCLUDED_TAGS']:
            if key in os.environ:
                del os.environ[key]
    
    @patch('lambda_function.ec2.describe_instances')
    def test_get_target_instances_success(self, mock_describe_instances):
        """Test successful retrieval of target instances."""
        # Mock EC2 response
        mock_describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-1234567890abcdef0',
                            'State': {'Name': 'running'},
                            'Tags': [
                                {'Key': 'Environment', 'Value': 'test'},
                                {'Key': 'Team', 'Value': 'platform'}
                            ]
                        },
                        {
                            'InstanceId': 'i-0987654321fedcba0',
                            'State': {'Name': 'running'},
                            'Tags': [
                                {'Key': 'Environment', 'Value': 'production'},
                                {'Key': 'Team', 'Value': 'platform'}
                            ]
                        }
                    ]
                }
            ]
        }
        
        instances = self.monkey.get_target_instances()
        
        # Should only return the instance that matches included tags
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0], 'i-1234567890abcdef0')
    
    @patch('lambda_function.ec2.describe_instances')
    def test_get_target_instances_excluded_tags(self, mock_describe_instances):
        """Test that instances with excluded tags are filtered out."""
        # Mock EC2 response with excluded tag
        mock_describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-1234567890abcdef0',
                            'State': {'Name': 'running'},
                            'Tags': [
                                {'Key': 'Environment', 'Value': 'test'},
                                {'Key': 'Critical', 'Value': 'true'}
                            ]
                        }
                    ]
                }
            ]
        }
        
        instances = self.monkey.get_target_instances()
        
        # Should return empty list due to excluded tag
        self.assertEqual(len(instances), 0)
    
    def test_should_trigger_chaos_probability(self):
        """Test chaos triggering probability."""
        # Test with gentle level (1%)
        self.monkey.chaos_level = 'gentle'
        self.monkey.probability = 1
        
        # With dry run enabled, should always return False for actual chaos
        self.assertTrue(self.monkey.dry_run)
        
        # Test with different random values
        with patch('lambda_function.random.randint') as mock_randint:
            mock_randint.return_value = 1
            self.assertTrue(self.monkey.should_trigger_chaos())
            
            mock_randint.return_value = 50
            self.assertFalse(self.monkey.should_trigger_chaos())
    
    def test_select_chaos_type(self):
        """Test chaos type selection."""
        chaos_type = self.monkey.select_chaos_type()
        self.assertIn(chaos_type, ['instance_termination', 'instance_stop', 'network_latency', 'cpu_stress', 'memory_stress', 'disk_io_stress'])
    
    @patch('lambda_function.ec2.terminate_instances')
    def test_terminate_instance_dry_run(self, mock_terminate):
        """Test instance termination in dry run mode."""
        success, error = self.monkey.terminate_instance('i-1234567890abcdef0')
        
        # Should succeed in dry run mode
        self.assertTrue(success)
        self.assertIsNone(error)
        
        # Should not call actual AWS API
        mock_terminate.assert_not_called()
    
    @patch('lambda_function.ec2.terminate_instances')
    def test_terminate_instance_real(self, mock_terminate):
        """Test instance termination in real mode."""
        # Disable dry run
        self.monkey.dry_run = False
        
        # Mock successful termination
        mock_terminate.return_value = {}
        
        success, error = self.monkey.terminate_instance('i-1234567890abcdef0')
        
        self.assertTrue(success)
        self.assertIsNone(error)
        mock_terminate.assert_called_once_with(InstanceIds=['i-1234567890abcdef0'])
    
    @patch('lambda_function.ec2.terminate_instances')
    def test_terminate_instance_failure(self, mock_terminate):
        """Test instance termination failure."""
        # Disable dry run
        self.monkey.dry_run = False
        
        # Mock termination failure
        mock_terminate.side_effect = Exception("Instance not found")
        
        success, error = self.monkey.terminate_instance('i-1234567890abcdef0')
        
        self.assertFalse(success)
        self.assertEqual(error, "Instance not found")
    
    def test_execute_chaos_unknown_type(self):
        """Test execution of unknown chaos type."""
        success, error = self.monkey.execute_chaos('i-1234567890abcdef0', 'unknown_chaos')
        
        self.assertFalse(success)
        self.assertEqual(error, "Unknown chaos type: unknown_chaos")
    
    def test_has_excluded_tags(self):
        """Test excluded tags filtering."""
        instance = {
            'Tags': [
                {'Key': 'Environment', 'Value': 'test'},
                {'Key': 'Critical', 'Value': 'true'}
            ]
        }
        
        result = self.monkey._has_excluded_tags(instance)
        self.assertTrue(result)
        
        # Test with no excluded tags
        instance_no_excluded = {
            'Tags': [
                {'Key': 'Environment', 'Value': 'test'}
            ]
        }
        
        result = self.monkey._has_excluded_tags(instance_no_excluded)
        self.assertFalse(result)
    
    def test_matches_included_tags(self):
        """Test included tags matching."""
        instance = {
            'Tags': [
                {'Key': 'Environment', 'Value': 'test'},
                {'Key': 'Team', 'Value': 'platform'}
            ]
        }
        
        result = self.monkey._matches_included_tags(instance)
        self.assertTrue(result)
        
        # Test with mismatched tags
        instance_mismatched = {
            'Tags': [
                {'Key': 'Environment', 'Value': 'production'},
                {'Key': 'Team', 'Value': 'platform'}
            ]
        }
        
        result = self.monkey._matches_included_tags(instance_mismatched)
        self.assertFalse(result)
    
    def test_chaos_probabilities(self):
        """Test chaos probability calculation."""
        # Test gentle level
        self.monkey.chaos_level = 'gentle'
        self.assertEqual(self.monkey.probability, 1)
        
        # Test medium level
        self.monkey.chaos_level = 'medium'
        self.assertEqual(self.monkey.probability, 5)
        
        # Test extreme level
        self.monkey.chaos_level = 'extreme'
        self.assertEqual(self.monkey.probability, 15)
        
        # Test invalid level (should default to 5)
        self.monkey.chaos_level = 'invalid'
        self.assertEqual(self.monkey.probability, 5)


class TestLambdaHandler(unittest.TestCase):
    """Test cases for the Lambda handler."""
    
    @patch('lambda_function.ChaosMonkey')
    def test_handler_success(self, mock_chaos_monkey):
        """Test successful handler execution."""
        # Mock chaos monkey
        mock_instance = Mock()
        mock_instance.should_trigger_chaos.return_value = True
        mock_instance.get_target_instances.return_value = ['i-1234567890abcdef0']
        mock_instance.select_chaos_type.return_value = 'instance_termination'
        mock_instance.execute_chaos.return_value = (True, None)
        mock_chaos_monkey.return_value = mock_instance
        
        # Mock event
        event = {
            'source': 'aws.events',
            'detail-type': 'Scheduled Event',
            'time': '2023-01-01T00:00:00Z'
        }
        
        # Call handler
        result = handler(event, None)
        
        # Verify result
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['message'], 'Chaos executed successfully')
        self.assertEqual(body['instance_id'], 'i-1234567890abcdef0')
        self.assertEqual(body['chaos_type'], 'instance_termination')
    
    @patch('lambda_function.ChaosMonkey')
    def test_handler_no_chaos_triggered(self, mock_chaos_monkey):
        """Test handler when no chaos is triggered."""
        # Mock chaos monkey
        mock_instance = Mock()
        mock_instance.should_trigger_chaos.return_value = False
        mock_chaos_monkey.return_value = mock_instance
        
        # Mock event
        event = {
            'source': 'aws.events',
            'detail-type': 'Scheduled Event',
            'time': '2023-01-01T00:00:00Z'
        }
        
        # Call handler
        result = handler(event, None)
        
        # Verify result
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['message'], 'No chaos triggered this time')
    
    @patch('lambda_function.ChaosMonkey')
    def test_handler_error(self, mock_chaos_monkey):
        """Test handler error handling."""
        # Mock chaos monkey to raise exception
        mock_chaos_monkey.side_effect = Exception("Test error")
        
        # Mock event
        event = {
            'source': 'aws.events',
            'detail-type': 'Scheduled Event',
            'time': '2023-01-01T00:00:00Z'
        }
        
        # Call handler
        result = handler(event, None)
        
        # Verify error result
        self.assertEqual(result['statusCode'], 500)
        body = json.loads(result['body'])
        self.assertIn('Handler error', body['error'])


if __name__ == '__main__':
    unittest.main()
