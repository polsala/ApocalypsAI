import unittest
import json
import os
from unittest.mock import patch, MagicMock
import sys

# Add the lambda directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))

from index import ChaosMonkey, handler


class TestChaosMonkey(unittest.TestCase):
    """Test cases for the ChaosMonkey class"""
    
    def setUp(self):
        """Set up test environment"""
        # Mock environment variables
        os.environ['DESTRUCTION_PROBABILITY'] = '0.5'
        os.environ['TARGET_RESOURCE_TYPES'] = 'aws_instance,aws_rds_instance'
        os.environ['SAFE_MODE'] = 'true'
        os.environ['MAX_RESOURCES_PER_RUN'] = '3'
        os.environ['EXCLUDED_RESOURCES'] = 'excluded-1,excluded-2'
        os.environ['AWS_REGION'] = 'us-east-1'
        
        self.chaos_monkey = ChaosMonkey()
    
    def tearDown(self):
        """Clean up test environment"""
        # Remove test environment variables
        for key in ['DESTRUCTION_PROBABILITY', 'TARGET_RESOURCE_TYPES', 'SAFE_MODE', 
                   'MAX_RESOURCES_PER_RUN', 'EXCLUDED_RESOURCES', 'AWS_REGION']:
            if key in os.environ:
                del os.environ[key]
    
    @patch('random.random')
    def test_should_execute_chaos_true(self, mock_random):
        """Test that chaos execution returns True when random value is below threshold"""
        mock_random.return_value = 0.3  # Below 0.5 threshold
        self.assertTrue(self.chaos_monkey.should_execute_chaos())
    
    @patch('random.random')
    def test_should_execute_chaos_false(self, mock_random):
        """Test that chaos execution returns False when random value is above threshold"""
        mock_random.return_value = 0.7  # Above 0.5 threshold
        self.assertFalse(self.chaos_monkey.should_execute_chaos())
    
    @patch('index.ec2_client.describe_instances')
    def test_get_ec2_instances(self, mock_describe):
        """Test EC2 instance discovery"""
        mock_describe.return_value = {
            'Reservations': [{
                'Instances': [{
                    'InstanceId': 'i-12345',
                    'State': {'Name': 'running'},
                    'LaunchTime': MagicMock(),
                    'Tags': [{'Key': 'Name', 'Value': 'test-instance'}]
                }]
            }]
        }
        
        instances = self.chaos_monkey._get_ec2_instances()
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0]['id'], 'i-12345')
        self.assertEqual(instances[0]['type'], 'aws_instance')
    
    @patch('index.ec2_client.describe_instances')
    def test_get_ec2_instances_excluded(self, mock_describe):
        """Test that excluded EC2 instances are filtered out"""
        mock_describe.return_value = {
            'Reservations': [{
                'Instances': [{
                    'InstanceId': 'excluded-1',  # This should be excluded
                    'State': {'Name': 'running'},
                    'LaunchTime': MagicMock(),
                    'Tags': [{'Key': 'Name', 'Value': 'excluded-instance'}]
                }, {
                    'InstanceId': 'i-12345',
                    'State': {'Name': 'running'},
                    'LaunchTime': MagicMock(),
                    'Tags': [{'Key': 'Name', 'Value': 'test-instance'}]
                }]
            }]
        }
        
        instances = self.chaos_monkey._get_ec2_instances()
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0]['id'], 'i-12345')
    
    @patch('index.ec2_client.describe_instances')
    def test_get_ec2_instances_chaos_monkey_exclude_tag(self, mock_describe):
        """Test that instances with chaos-monkey-exclude tag are filtered out"""
        mock_describe.return_value = {
            'Reservations': [{
                'Instances': [{
                    'InstanceId': 'i-12345',
                    'State': {'Name': 'running'},
                    'LaunchTime': MagicMock(),
                    'Tags': [{'Key': 'chaos-monkey-exclude', 'Value': 'true'}]
                }]
            }]
        }
        
        instances = self.chaos_monkey._get_ec2_instances()
        self.assertEqual(len(instances), 0)
    
    @patch('index.rds_client.describe_db_instances')
    @patch('index.rds_client.list_tags_for_resource')
    def test_get_rds_instances(self, mock_list_tags, mock_describe):
        """Test RDS instance discovery"""
        mock_describe.return_value = {
            'DBInstances': [{
                'DBInstanceIdentifier': 'db-test',
                'DBInstanceStatus': 'available',
                'Engine': 'mysql',
                'AllocatedStorage': 20,
                'DBInstanceArn': 'arn:aws:rds:us-east-1:123456789012:db:db-test'
            }]
        }
        mock_list_tags.return_value = {'TagList': []}
        
        instances = self.chaos_monkey._get_rds_instances()
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0]['id'], 'db-test')
        self.assertEqual(instances[0]['type'], 'aws_rds_instance')
    
    @patch('index.s3_client.list_buckets')
    @patch('index.s3_client.get_bucket_tagging')
    def test_get_s3_buckets(self, mock_get_tags, mock_list):
        """Test S3 bucket discovery"""
        mock_list.return_value = {
            'Buckets': [{
                'Name': 'test-bucket',
                'CreationDate': MagicMock()
            }]
        }
        mock_get_tags.return_value = {'TagSet': []}
        
        buckets = self.chaos_monkey._get_s3_buckets()
        self.assertEqual(len(buckets), 1)
        self.assertEqual(buckets[0]['id'], 'test-bucket')
        self.assertEqual(buckets[0]['type'], 'aws_s3_bucket')
    
    @patch('index.lambda_client.list_functions')
    @patch('index.lambda_client.list_tags')
    def test_get_lambda_functions(self, mock_list_tags, mock_list):
        """Test Lambda function discovery"""
        mock_list.return_value = {
            'Functions': [{
                'FunctionName': 'test-function',
                'Runtime': 'python3.9',
                'MemorySize': 128,
                'FunctionArn': 'arn:aws:lambda:us-east-1:123456789012:function:test-function'
            }]
        }
        mock_list_tags.return_value = {'Tags': {}}
        
        functions = self.chaos_monkey._get_lambda_functions()
        self.assertEqual(len(functions), 1)
        self.assertEqual(functions[0]['id'], 'test-function')
        self.assertEqual(functions[0]['type'], 'aws_lambda_function')
    
    def test_select_resources_for_chaos(self):
        """Test resource selection for chaos"""
        resources = [
            {'id': 'i-1', 'type': 'aws_instance'},
            {'id': 'i-2', 'type': 'aws_instance'},
            {'id': 'i-3', 'type': 'aws_instance'}
        ]
        
        with patch('random.sample') as mock_sample:
            mock_sample.return_value = [resources[0], resources[1]]
            selected = self.chaos_monkey.select_resources_for_chaos(resources)
            
            self.assertEqual(len(selected), 2)
            mock_sample.assert_called_once()
    
    def test_select_resources_for_chaos_empty(self):
        """Test resource selection with empty list"""
        selected = self.chaos_monkey.select_resources_for_chaos([])
        self.assertEqual(len(selected), 0)
    
    @patch('index.ec2_client.stop_instances')
    @patch('index.ec2_client.terminate_instances')
    @patch('index.ec2_client.get_waiter')
    def test_destroy_ec2_instance_safe_mode(self, mock_waiter, mock_terminate, mock_stop):
        """Test EC2 instance destruction in safe mode"""
        mock_waiter.return_value.wait = MagicMock()
        
        resource = {'id': 'i-12345', 'type': 'aws_instance'}
        result = self.chaos_monkey.destroy_resource(resource)
        
        self.assertTrue(result['success'])
        self.assertIn('[SAFE MODE]', result['message'])
        mock_stop.assert_not_called()
        mock_terminate.assert_not_called()
    
    @patch('index.ec2_client.stop_instances')
    @patch('index.ec2_client.terminate_instances')
    @patch('index.ec2_client.get_waiter')
    def test_destroy_ec2_instance_real_mode(self, mock_waiter, mock_terminate, mock_stop):
        """Test EC2 instance destruction in real mode"""
        # Disable safe mode
        self.chaos_monkey.safe_mode = False
        mock_waiter.return_value.wait = MagicMock()
        
        resource = {'id': 'i-12345', 'type': 'aws_instance'}
        result = self.chaos_monkey.destroy_resource(resource)
        
        self.assertTrue(result['success'])
        self.assertNotIn('[SAFE MODE]', result['message'])
        mock_stop.assert_called_once_with(InstanceIds=['i-12345'])
        mock_terminate.assert_called_once_with(InstanceIds=['i-12345'])
    
    def test_destroy_unknown_resource_type(self):
        """Test destruction of unknown resource type"""
        resource = {'id': 'unknown-123', 'type': 'unknown_type'}
        result = self.chaos_monkey.destroy_resource(resource)
        
        self.assertFalse(result['success'])
        self.assertIn('Unknown resource type', result['error'])
    
    @patch('index.ChaosMonkey.get_targetable_resources')
    @patch('index.ChaosMonkey.select_resources_for_chaos')
    @patch('index.ChaosMonkey.destroy_resource')
    def test_execute_chaos_no_resources(self, mock_destroy, mock_select, mock_get_resources):
        """Test chaos execution with no targetable resources"""
        mock_get_resources.return_value = []
        mock_select.return_value = []
        mock_destroy.return_value = {'success': True}
        
        result = self.chaos_monkey.execute_chaos()
        
        self.assertTrue(result['executed'])
        self.assertEqual(result['resources_found'], 0)
        self.assertEqual(result['resources_destroyed'], 0)
    
    @patch('index.ChaosMonkey.get_targetable_resources')
    @patch('index.ChaosMonkey.select_resources_for_chaos')
    @patch('index.ChaosMonkey.destroy_resource')
    def test_execute_chaos_with_resources(self, mock_destroy, mock_select, mock_get_resources):
        """Test chaos execution with targetable resources"""
        resources = [{'id': 'i-1', 'type': 'aws_instance'}]
        selected = [{'id': 'i-1', 'type': 'aws_instance'}]
        destroy_result = {'success': True, 'message': 'Destroyed'}
        
        mock_get_resources.return_value = resources
        mock_select.return_value = selected
        mock_destroy.return_value = destroy_result
        
        result = self.chaos_monkey.execute_chaos()
        
        self.assertTrue(result['executed'])
        self.assertEqual(result['resources_found'], 1)
        self.assertEqual(result['resources_selected'], 1)
        self.assertEqual(result['resources_destroyed'], 1)


class TestHandler(unittest.TestCase):
    """Test cases for the Lambda handler function"""
    
    @patch('index.ChaosMonkey')
    def test_handler_success(self, mock_chaos_monkey):
        """Test successful handler execution"""
        mock_instance = MagicMock()
        mock_instance.execute_chaos.return_value = {'success': True}
        mock_chaos_monkey.return_value = mock_instance
        
        event = {'source': 'aws.events'}
        context = MagicMock()
        
        result = handler(event, context)
        
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('success', json.loads(result['body']))
    
    @patch('index.ChaosMonkey')
    def test_handler_exception(self, mock_chaos_monkey):
        """Test handler execution with exception"""
        mock_chaos_monkey.side_effect = Exception("Test error")
        
        event = {'source': 'aws.events'}
        context = MagicMock()
        
        result = handler(event, context)
        
        self.assertEqual(result['statusCode'], 500)
        self.assertIn('Test error', json.loads(result['body'])['error'])


if __name__ == '__main__':
    unittest.main()
