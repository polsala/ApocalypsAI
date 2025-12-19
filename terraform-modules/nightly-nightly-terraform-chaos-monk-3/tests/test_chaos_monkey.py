import unittest
import json
import os
from unittest.mock import patch, MagicMock
import sys

# Add the lambda directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))

# Import the handler module
import index


class TestChaosMonkey(unittest.TestCase):
    """
    Test cases for the chaos monkey lambda function.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        """
        # Mock environment variables
        os.environ['CHAOS_INTERVAL'] = '60'
        os.environ['TARGET_RESOURCE_TYPES'] = 'aws_instance,aws_rds_instance'
        os.environ['PROTECTED_RESOURCES'] = 'protected-db,critical-api'
        os.environ['MAX_DESTRUCTIONS_PER_CYCLE'] = '2'
        os.environ['DRY_RUN'] = 'true'
        os.environ['AWS_REGION'] = 'us-east-1'
    
    def tearDown(self):
        """
        Clean up after tests.
        """
        # Remove test environment variables
        for key in ['CHAOS_INTERVAL', 'TARGET_RESOURCE_TYPES', 'PROTECTED_RESOURCES', 
                   'MAX_DESTRUCTIONS_PER_CYCLE', 'DRY_RUN', 'AWS_REGION']:
            if key in os.environ:
                del os.environ[key]
    
    @patch('index.ec2_client')
    @patch('index.rds_client')
    @patch('index.lambda_client')
    def test_handler_success(self, mock_lambda_client, mock_rds_client, mock_ec2_client):
        """
        Test successful execution of the chaos monkey handler.
        """
        # Mock EC2 client
        mock_ec2_client.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-1234567890abcdef0',
                            'InstanceType': 't2.micro',
                            'State': {'Name': 'running'},
                            'Tags': [
                                {'Key': 'Name', 'Value': 'test-instance-1'}
                            ]
                        },
                        {
                            'InstanceId': 'i-1234567890abcdef1',
                            'InstanceType': 't2.micro',
                            'State': {'Name': 'running'},
                            'Tags': [
                                {'Key': 'Name', 'Value': 'protected-db'}
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Mock RDS client
        mock_rds_client.describe_db_instances.return_value = {
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'test-db-1',
                    'DBInstanceStatus': 'available'
                },
                {
                    'DBInstanceIdentifier': 'protected-db',
                    'DBInstanceStatus': 'available'
                }
            ]
        }
        
        # Mock Lambda client
        mock_lambda_client.list_functions.return_value = {
            'Functions': [
                {'FunctionName': 'test-function-1'},
                {'FunctionName': 'chaos-monkey-test'}
            ]
        }
        
        # Execute handler
        result = index.handler({}, {})
        
        # Verify results
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['message'], 'Chaos Monkey executed successfully')
        self.assertTrue(body['summary']['dry_run'])
        
        # Verify that EC2 describe_instances was called
        mock_ec2_client.describe_instances.assert_called_once()
        
        # Verify that RDS describe_db_instances was called
        mock_rds_client.describe_db_instances.assert_called_once()
        
        # Verify that Lambda list_functions was called
        mock_lambda_client.list_functions.assert_called_once()
    
    @patch('index.ec2_client')
    def test_chaos_ec2_instances_dry_run(self, mock_ec2_client):
        """
        Test EC2 chaos in dry run mode.
        """
        # Mock EC2 client
        mock_ec2_client.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-1234567890abcdef0',
                            'InstanceType': 't2.micro',
                            'State': {'Name': 'running'},
                            'Tags': [
                                {'Key': 'Name', 'Value': 'test-instance-1'}
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Execute chaos_ec2_instances
        results = index.chaos_ec2_instances(['protected-db'], 1, True)
        
        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['action'], 'would_destroy')
        self.assertEqual(results[0]['resource_id'], 'i-1234567890abcdef0')
        self.assertTrue(results[0]['resource_name'], 'test-instance-1')
        
        # Verify that terminate_instances was NOT called (dry run)
        mock_ec2_client.terminate_instances.assert_not_called()
    
    @patch('index.ec2_client')
    def test_chaos_ec2_instances_protected(self, mock_ec2_client):
        """
        Test that protected EC2 instances are not targeted.
        """
        # Mock EC2 client
        mock_ec2_client.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-1234567890abcdef0',
                            'InstanceType': 't2.micro',
                            'State': {'Name': 'running'},
                            'Tags': [
                                {'Key': 'Name', 'Value': 'protected-db'}
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Execute chaos_ec2_instances
        results = index.chaos_ec2_instances(['protected-db'], 1, False)
        
        # Verify results - no actions should be taken
        self.assertEqual(len(results), 0)
        
        # Verify that terminate_instances was NOT called
        mock_ec2_client.terminate_instances.assert_not_called()
    
    @patch('index.rds_client')
    def test_chaos_rds_instances_dry_run(self, mock_rds_client):
        """
        Test RDS chaos in dry run mode.
        """
        # Mock RDS client
        mock_rds_client.describe_db_instances.return_value = {
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'test-db-1',
                    'DBInstanceStatus': 'available'
                }
            ]
        }
        
        # Execute chaos_rds_instances
        results = index.chaos_rds_instances(['protected-db'], 1, True)
        
        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['action'], 'would_destroy')
        self.assertEqual(results[0]['resource_id'], 'test-db-1')
        
        # Verify that delete_db_instance was NOT called (dry run)
        mock_rds_client.delete_db_instance.assert_not_called()
    
    @patch('index.rds_client')
    def test_chaos_rds_instances_protected(self, mock_rds_client):
        """
        Test that protected RDS instances are not targeted.
        """
        # Mock RDS client
        mock_rds_client.describe_db_instances.return_value = {
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'protected-db',
                    'DBInstanceStatus': 'available'
                }
            ]
        }
        
        # Execute chaos_rds_instances
        results = index.chaos_rds_instances(['protected-db'], 1, False)
        
        # Verify results - no actions should be taken
        self.assertEqual(len(results), 0)
        
        # Verify that delete_db_instance was NOT called
        mock_rds_client.delete_db_instance.assert_not_called()
    
    @patch('index.lambda_client')
    def test_chaos_lambda_functions_dry_run(self, mock_lambda_client):
        """
        Test Lambda chaos in dry run mode.
        """
        # Mock Lambda client
        mock_lambda_client.list_functions.return_value = {
            'Functions': [
                {'FunctionName': 'test-function-1'},
                {'FunctionName': 'test-function-2'}
            ]
        }
        
        # Execute chaos_lambda_functions
        results = index.chaos_lambda_functions(['protected-function'], 2, True)
        
        # Verify results
        self.assertEqual(len(results), 2)
        for result in results:
            self.assertEqual(result['action'], 'would_destroy')
            self.assertIn(result['resource_name'], ['test-function-1', 'test-function-2'])
        
        # Verify that delete_function was NOT called (dry run)
        mock_lambda_client.delete_function.assert_not_called()
    
    @patch('index.lambda_client')
    def test_chaos_lambda_functions_protected(self, mock_lambda_client):
        """
        Test that protected Lambda functions are not targeted.
        """
        # Mock Lambda client
        mock_lambda_client.list_functions.return_value = {
            'Functions': [
                {'FunctionName': 'protected-function'},
                {'FunctionName': 'chaos-monkey-test'}
            ]
        }
        
        # Execute chaos_lambda_functions
        results = index.chaos_lambda_functions(['protected-function'], 2, False)
        
        # Verify results - no actions should be taken
        self.assertEqual(len(results), 0)
        
        # Verify that delete_function was NOT called
        mock_lambda_client.delete_function.assert_not_called()
    
    @patch('index.ec2_client')
    def test_chaos_ec2_instances_error_handling(self, mock_ec2_client):
        """
        Test error handling in EC2 chaos.
        """
        # Mock EC2 client to raise an exception
        mock_ec2_client.describe_instances.side_effect = Exception("Test error")
        
        # Execute chaos_ec2_instances
        results = index.chaos_ec2_instances([], 1, False)
        
        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['action'], 'error')
        self.assertIn('Test error', results[0]['error'])
    
    def test_handler_environment_variables(self):
        """
        Test that environment variables are correctly parsed.
        """
        # Test with different environment variable values
        os.environ['CHAOS_INTERVAL'] = '120'
        os.environ['TARGET_RESOURCE_TYPES'] = 'aws_instance'
        os.environ['PROTECTED_RESOURCES'] = 'db1,db2'
        os.environ['MAX_DESTRUCTIONS_PER_CYCLE'] = '5'
        os.environ['DRY_RUN'] = 'false'
        os.environ['AWS_REGION'] = 'us-west-2'
        
        # Mock the chaos functions to avoid actual AWS calls
        with patch('index.chaos_ec2_instances') as mock_ec2, \
             patch('index.chaos_rds_instances') as mock_rds, \
             patch('index.chaos_lambda_functions') as mock_lambda:
            
            mock_ec2.return_value = []
            mock_rds.return_value = []
            mock_lambda.return_value = []
            
            result = index.handler({}, {})
            
            # Verify that the handler executed successfully
            self.assertEqual(result['statusCode'], 200)
            body = json.loads(result['body'])
            self.assertFalse(body['summary']['dry_run'])
            self.assertEqual(body['summary']['max_destructions'], 5)


if __name__ == '__main__':
    unittest.main()
