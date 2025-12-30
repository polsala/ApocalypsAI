import unittest
import json
import os
from unittest.mock import patch, MagicMock
import sys

# Add the lambda directory to the path so we can import the module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))

# Import the lambda handler
import index


class TestChaosMonkey(unittest.TestCase):
    """
    Unit tests for the chaos monkey Lambda function.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        # Mock environment variables
        os.environ['CHAOS_PROBABILITY'] = '0.5'  # High probability for testing
        os.environ['TARGET_RESOURCE_TYPES'] = 'aws_instance,aws_rds_instance'
        os.environ['EXCLUDED_TAGS'] = '{"environment": "critical"}'
        os.environ['SAFE_MODE'] = 'true'
        os.environ['TIME_WINDOW_START'] = '9'
        os.environ['TIME_WINDOW_END'] = '17'
        
        # Mock AWS clients
        self.mock_ec2_client = MagicMock()
        self.mock_rds_client = MagicMock()
        self.mock_cloudwatch = MagicMock()
        
    def tearDown(self):
        """
        Clean up test fixtures.
        """
        # Remove test environment variables
        for key in ['CHAOS_PROBABILITY', 'TARGET_RESOURCE_TYPES', 'EXCLUDED_TAGS', 
                   'SAFE_MODE', 'TIME_WINDOW_START', 'TIME_WINDOW_END']:
            if key in os.environ:
                del os.environ[key]
    
    @patch('index.ec2_client')
    @patch('index.rds_client')
    @patch('index.cloudwatch')
    @patch('index.datetime')
    def test_outside_time_window(self, mock_datetime, mock_cloudwatch, mock_rds_client, mock_ec2_client):
        """
        Test that chaos is skipped when outside the time window.
        """
        # Mock current time to be outside the window
        mock_datetime.now.return_value.hour = 20  # Outside 9-17 window
        
        event = {}
        context = MagicMock()
        
        result = index.lambda_handler(event, context)
        
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('Outside time window', json.loads(result['body'])['message'])
        
        # Verify no AWS calls were made
        mock_ec2_client.describe_instances.assert_not_called()
        mock_rds_client.describe_db_instances.assert_not_called()
    
    @patch('index.ec2_client')
    @patch('index.rds_client')
    @patch('index.cloudwatch')
    @patch('index.datetime')
    @patch('index.random')
    def test_chaos_probability_not_met(self, mock_random, mock_datetime, mock_cloudwatch, mock_rds_client, mock_ec2_client):
        """
        Test that chaos is skipped when probability threshold is not met.
        """
        # Mock current time to be inside the window
        mock_datetime.now.return_value.hour = 12  # Inside 9-17 window
        
        # Mock random to return a value higher than our probability (0.5)
        mock_random.random.return_value = 0.8
        
        event = {}
        context = MagicMock()
        
        result = index.lambda_handler(event, context)
        
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('Chaos probability not met', json.loads(result['body'])['message'])
        
        # Verify no AWS calls were made
        mock_ec2_client.describe_instances.assert_not_called()
        mock_rds_client.describe_db_instances.assert_not_called()
    
    @patch('index.ec2_client')
    @patch('index.rds_client')
    @patch('index.cloudwatch')
    @patch('index.datetime')
    @patch('index.random')
    def test_chaos_execution_safe_mode(self, mock_random, mock_datetime, mock_cloudwatch, mock_rds_client, mock_ec2_client):
        """
        Test chaos execution in safe mode (dry run).
        """
        # Mock current time to be inside the window
        mock_datetime.now.return_value.hour = 12  # Inside 9-17 window
        
        # Mock random to return a value lower than our probability (0.5)
        mock_random.random.return_value = 0.3
        
        # Mock EC2 instances
        mock_ec2_client.describe_instances.return_value = {
            'Reservations': [{
                'Instances': [{
                    'InstanceId': 'i-1234567890abcdef0',
                    'State': {'Name': 'running'},
                    'Tags': [{'Key': 'Environment', 'Value': 'test'}]
                }]
            }]
        }
        
        # Mock RDS instances
        mock_rds_client.describe_db_instances.return_value = {
            'DBInstances': [{
                'DBInstanceIdentifier': 'test-db',
                'DBInstanceArn': 'arn:aws:rds:us-east-1:123456789012:db:test-db',
                'DBInstanceStatus': 'available'
            }]
        }
        
        # Mock list_tags_for_resource
        mock_rds_client.list_tags_for_resource.return_value = {
            'TagList': [{'Key': 'Environment', 'Value': 'test'}]
        }
        
        event = {}
        context = MagicMock()
        
        result = index.lambda_handler(event, context)
        
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertIn('Chaos executed successfully', body['message'])
        
        # Verify that instances were found but not actually terminated (safe mode)
        mock_ec2_client.describe_instances.assert_called_once()
        mock_rds_client.describe_db_instances.assert_called_once()
        
        # Verify that terminate_instances was NOT called (safe mode)
        mock_ec2_client.terminate_instances.assert_not_called()
        mock_rds_client.delete_db_instance.assert_not_called()
        
        # Verify metrics were sent
        mock_cloudwatch.put_metric_data.assert_called_once()
    
    @patch('index.ec2_client')
    @patch('index.rds_client')
    @patch('index.cloudwatch')
    @patch('index.datetime')
    @patch('index.random')
    def test_chaos_execution_live_mode(self, mock_random, mock_datetime, mock_cloudwatch, mock_rds_client, mock_ec2_client):
        """
        Test chaos execution in live mode (actual termination).
        """
        # Set safe mode to false
        os.environ['SAFE_MODE'] = 'false'
        
        # Mock current time to be inside the window
        mock_datetime.now.return_value.hour = 12  # Inside 9-17 window
        
        # Mock random to return a value lower than our probability (0.5)
        mock_random.random.return_value = 0.3
        
        # Mock EC2 instances
        mock_ec2_client.describe_instances.return_value = {
            'Reservations': [{
                'Instances': [{
                    'InstanceId': 'i-1234567890abcdef0',
                    'State': {'Name': 'running'},
                    'Tags': [{'Key': 'Environment', 'Value': 'test'}]
                }]
            }]
        }
        
        # Mock RDS instances
        mock_rds_client.describe_db_instances.return_value = {
            'DBInstances': [{
                'DBInstanceIdentifier': 'test-db',
                'DBInstanceArn': 'arn:aws:rds:us-east-1:123456789012:db:test-db',
                'DBInstanceStatus': 'available'
            }]
        }
        
        # Mock list_tags_for_resource
        mock_rds_client.list_tags_for_resource.return_value = {
            'TagList': [{'Key': 'Environment', 'Value': 'test'}]
        }
        
        event = {}
        context = MagicMock()
        
        result = index.lambda_handler(event, context)
        
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertIn('Chaos executed successfully', body['message'])
        
        # Verify that instances were found and terminated (live mode)
        mock_ec2_client.describe_instances.assert_called_once()
        mock_rds_client.describe_db_instances.assert_called_once()
        
        # Verify that terminate_instances WAS called (live mode)
        mock_ec2_client.terminate_instances.assert_called_once_with(
            InstanceIds=['i-1234567890abcdef0']
        )
        mock_rds_client.delete_db_instance.assert_called_once_with(
            DBInstanceIdentifier='test-db',
            SkipFinalSnapshot=True,
            DeleteAutomatedBackups=True
        )
        
        # Verify metrics were sent
        mock_cloudwatch.put_metric_data.assert_called_once()
    
    @patch('index.ec2_client')
    @patch('index.rds_client')
    @patch('index.cloudwatch')
    @patch('index.datetime')
    @patch('index.random')
    def test_chaos_with_excluded_tags(self, mock_random, mock_datetime, mock_cloudwatch, mock_rds_client, mock_ec2_client):
        """
        Test that resources with excluded tags are not targeted.
        """
        # Mock current time to be inside the window
        mock_datetime.now.return_value.hour = 12  # Inside 9-17 window
        
        # Mock random to return a value lower than our probability (0.5)
        mock_random.random.return_value = 0.3
        
        # Mock EC2 instances - one with excluded tag, one without
        mock_ec2_client.describe_instances.return_value = {
            'Reservations': [{
                'Instances': [
                    {
                        'InstanceId': 'i-1234567890abcdef0',
                        'State': {'Name': 'running'},
                        'Tags': [{'Key': 'environment', 'Value': 'critical'}]  # Excluded
                    },
                    {
                        'InstanceId': 'i-0987654321fedcba0',
                        'State': {'Name': 'running'},
                        'Tags': [{'Key': 'Environment', 'Value': 'test'}]  # Not excluded
                    }
                ]
            }]
        }
        
        # Mock RDS instances - one with excluded tag, one without
        mock_rds_client.describe_db_instances.return_value = {
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'critical-db',
                    'DBInstanceArn': 'arn:aws:rds:us-east-1:123456789012:db:critical-db',
                    'DBInstanceStatus': 'available'
                },
                {
                    'DBInstanceIdentifier': 'test-db',
                    'DBInstanceArn': 'arn:aws:rds:us-east-1:123456789012:db:test-db',
                    'DBInstanceStatus': 'available'
                }
            ]
        }
        
        # Mock list_tags_for_resource
        def mock_list_tags(ResourceName):
            if 'critical-db' in ResourceName:
                return {'TagList': [{'Key': 'environment', 'Value': 'critical'}]}
            else:
                return {'TagList': [{'Key': 'Environment', 'Value': 'test'}]}
        
        mock_rds_client.list_tags_for_resource.side_effect = mock_list_tags
        
        event = {}
        context = MagicMock()
        
        result = index.lambda_handler(event, context)
        
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertIn('Chaos executed successfully', body['message'])
        
        # Verify that only the non-excluded resources were targeted
        # The critical resources should be skipped
        mock_ec2_client.terminate_instances.assert_called_once_with(
            InstanceIds=['i-0987654321fedcba0']
        )
        mock_rds_client.delete_db_instance.assert_called_once_with(
            DBInstanceIdentifier='test-db',
            SkipFinalSnapshot=True,
            DeleteAutomatedBackups=True
        )
    
    def test_should_execute_chaos(self):
        """
        Test the should_execute_chaos function.
        """
        # Test with probability 1.0 (should always execute)
        self.assertTrue(index.should_execute_chaos(1.0))
        
        # Test with probability 0.0 (should never execute)
        self.assertFalse(index.should_execute_chaos(0.0))
        
        # Test with probability 0.5 (random)
        # We can't predict the exact outcome, but we can test that it returns a boolean
        result = index.should_execute_chaos(0.5)
        self.assertIsInstance(result, bool)
    
    def test_parse_environment_variables(self):
        """
        Test parsing of environment variables.
        """
        # Test default values
        self.assertEqual(float(os.environ.get('CHAOS_PROBABILITY', '0.01')), 0.5)  # Set in setUp
        self.assertEqual(os.environ.get('TARGET_RESOURCE_TYPES', 'aws_instance').split(','), 
                        ['aws_instance', 'aws_rds_instance'])
        self.assertEqual(json.loads(os.environ.get('EXCLUDED_TAGS', '{}')), 
                        {'environment': 'critical'})
        self.assertTrue(os.environ.get('SAFE_MODE', 'true').lower() == 'true')
        self.assertEqual(int(os.environ.get('TIME_WINDOW_START', '9')), 9)
        self.assertEqual(int(os.environ.get('TIME_WINDOW_END', '17')), 17)


if __name__ == '__main__':
    unittest.main()
