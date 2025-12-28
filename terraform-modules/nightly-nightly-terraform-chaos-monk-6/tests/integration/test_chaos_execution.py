import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os
import time
from datetime import datetime, timedelta

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chaos_lambda import lambda_handler


class TestChaosExecution(unittest.TestCase):
    """Integration tests for chaos execution"""
    
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
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_chaos_execution_full_coverage(self, mock_ecs, mock_rds, mock_ec2):
        """Test chaos execution with full resource coverage"""
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': f'i-{i:017x}',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': f'test-instance-{i}'}],
                'name': f'test-instance-{i}'
            } for i in range(10)
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        # Record start time
        start_time = datetime.now()
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Record end time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify execution
        self.assertEqual(body['total_resources'], 10)
        self.assertEqual(body['unprotected_resources'], 10)
        self.assertEqual(body['selected_for_termination'], 10)  # 100% intensity
        self.assertEqual(body['successful_terminations'], 10)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify execution time is reasonable
        self.assertLess(execution_time, 30)  # Should complete within 30 seconds
        
        # Verify all chaos events
        self.assertEqual(len(body['chaos_events']), 10)
        for event in body['chaos_events']:
            self.assertTrue(event['success'])
            self.assertEqual(event['action'], 'terminate')
            self.assertEqual(event['resource_type'], 'aws_instance')
    
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
    def test_chaos_execution_partial_coverage(self, mock_terminate, mock_ecs, mock_rds, mock_ec2):
        """Test chaos execution with partial resource coverage"""
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': f'i-{i:017x}',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': f'test-instance-{i}'}],
                'name': f'test-instance-{i}'
            } for i in range(20)
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        # Mock successful terminations
        mock_terminate.return_value = True
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify execution
        self.assertEqual(body['total_resources'], 20)
        self.assertEqual(body['unprotected_resources'], 20)
        self.assertEqual(body['selected_for_termination'], 10)  # 50% of 20
        self.assertEqual(body['successful_terminations'], 10)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify chaos events
        self.assertEqual(len(body['chaos_events']), 10)
        for event in body['chaos_events']:
            self.assertTrue(event['success'])
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '10',
        'TARGET_RESOURCES': '["aws_instance"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'false',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    @patch('src.chaos_lambda.terminate_ec2_instance')
    def test_chaos_execution_random_selection(self, mock_terminate, mock_ecs, mock_rds, mock_ec2):
        """Test that chaos execution randomly selects resources"""
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': f'i-{i:017x}',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': f'test-instance-{i}'}],
                'name': f'test-instance-{i}'
            } for i in range(100)
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        # Mock successful terminations
        mock_terminate.return_value = True
        
        # Run multiple times to verify randomness
        selected_resources = set()
        for _ in range(5):
            result = lambda_handler(self.test_event, self.test_context)
            body = json.loads(result['body'])
            
            for event in body['chaos_events']:
                selected_resources.add(event['resource_id'])
        
        # Should have selected different resources across runs
        self.assertGreater(len(selected_resources), 10)  # More than just 10 unique selections
    
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
    def test_chaos_execution_mixed_results(self, mock_terminate, mock_ecs, mock_rds, mock_ec2):
        """Test chaos execution with mixed success/failure results"""
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': f'i-{i:017x}',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': f'test-instance-{i}'}],
                'name': f'test-instance-{i}'
            } for i in range(10)
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        # Mock mixed termination results
        mock_terminate.side_effect = [True, False, True, False, True, False, True, False, True, False]
        
        result = lambda_handler(self.test_event, self.test_context)
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify execution
        self.assertEqual(body['total_resources'], 10)
        self.assertEqual(body['unprotected_resources'], 10)
        self.assertEqual(body['selected_for_termination'], 10)
        self.assertEqual(body['successful_terminations'], 5)
        self.assertEqual(body['failed_terminations'], 5)
        
        # Verify chaos events
        self.assertEqual(len(body['chaos_events']), 10)
        success_count = sum(1 for event in body['chaos_events'] if event['success'])
        self.assertEqual(success_count, 5)
    
    @patch.dict('os.environ', {
        'CHAOS_INTENSITY': '100',
        'TARGET_RESOURCES': '["aws_instance", "aws_rds_instance", "aws_ecs_service"]',
        'EXCLUDED_TAGS': '[]',
        'SAFE_MODE': 'true',
        'REGION': 'us-east-1'
    })
    @patch('src.chaos_lambda.get_ec2_instances')
    @patch('src.chaos_lambda.get_rds_instances')
    @patch('src.chaos_lambda.get_ecs_services')
    def test_chaos_execution_multiple_resource_types(self, mock_ecs, mock_rds, mock_ec2):
        """Test chaos execution with multiple resource types"""
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
        
        # Parse result
        body = json.loads(result['body'])
        
        # Verify execution
        self.assertEqual(body['total_resources'], 3)
        self.assertEqual(body['unprotected_resources'], 3)
        self.assertEqual(body['selected_for_termination'], 3)  # 100% intensity
        self.assertEqual(body['successful_terminations'], 3)
        self.assertEqual(body['failed_terminations'], 0)
        
        # Verify chaos events include all resource types
        resource_types = {event['resource_type'] for event in body['chaos_events']}
        self.assertIn('aws_instance', resource_types)
        self.assertIn('aws_rds_instance', resource_types)
        self.assertIn('aws_ecs_service', resource_types)
    
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
    def test_chaos_execution_timing_consistency(self, mock_ecs, mock_rds, mock_ec2):
        """Test that chaos execution timing is consistent"""
        # Mock resources
        mock_ec2.return_value = [
            {
                'id': f'i-{i:017x}',
                'type': 'aws_instance',
                'state': 'running',
                'tags': [{'Key': 'Name', 'Value': f'test-instance-{i}'}],
                'name': f'test-instance-{i}'
            } for i in range(50)
        ]
        mock_rds.return_value = []
        mock_ecs.return_value = []
        
        # Measure execution time over multiple runs
        execution_times = []
        for _ in range(3):
            start_time = time.time()
            result = lambda_handler(self.test_event, self.test_context)
            end_time = time.time()
            execution_times.append(end_time - start_time)
        
        # Verify consistency (standard deviation should be low)
        mean_time = sum(execution_times) / len(execution_times)
        variance = sum((t - mean_time) ** 2 for t in execution_times) / len(execution_times)
        std_dev = variance ** 0.5
        
        # Should be reasonably consistent (within 20% variation)
        self.assertLess(std_dev / mean_time, 0.2)
    
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
    def test_chaos_execution_empty_resources(self, mock_ecs, mock_rds, mock_ec2):
        """Test chaos execution with no resources"""
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


if __name__ == '__main__':
    unittest.main()
