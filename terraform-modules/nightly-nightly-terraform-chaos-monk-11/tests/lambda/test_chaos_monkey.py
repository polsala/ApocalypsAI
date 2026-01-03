import json
import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the lambda directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))

# Import the lambda function
import index


class TestChaosMonkey(unittest.TestCase):
    
    def setUp(self):
        # Mock environment variables
        self.mock_env = {
            'RESOURCE_TYPES': 'ec2,rds',
            'EXCLUDE_TAGS': json.dumps({'Environment': 'production'}),
            'MAX_CHAOS_PER_RUN': '3',
            'DRY_RUN': 'true',
            'AWS_REGION': 'us-east-1',
            'ENABLED': 'true'
        }
    
    @patch.dict('os.environ', {'RESOURCE_TYPES': 'ec2,rds'})
    def test_get_resource_types(self):
        """Test getting resource types from environment."""
        result = index.get_resource_types()
        expected = ['ec2', 'rds']
        self.assertEqual(result, expected)
    
    @patch.dict('os.environ', {'EXCLUDE_TAGS': '{"Environment": "production"}'})
    def test_get_exclude_tags(self):
        """Test getting exclude tags from environment."""
        result = index.get_exclude_tags()
        expected = {'Environment': 'production'}
        self.assertEqual(result, expected)
    
    def test_is_resource_excluded(self):
        """Test resource exclusion logic."""
        exclude_tags = {'Environment': 'production'}
        
        # Resource with excluded tag
        tags_with_excluded = [{'Key': 'Environment', 'Value': 'production'}]
        self.assertTrue(index.is_resource_excluded(tags_with_excluded, exclude_tags))
        
        # Resource without excluded tag
        tags_without_excluded = [{'Key': 'Environment', 'Value': 'staging'}]
        self.assertFalse(index.is_resource_excluded(tags_without_excluded, exclude_tags))
        
        # Empty tags
        self.assertFalse(index.is_resource_excluded([], exclude_tags))
    
    @patch('index.ec2_client.describe_instances')
    def test_get_ec2_instances(self, mock_describe):
        """Test EC2 instance discovery."""
        mock_response = {
            'Reservations': [{
                'Instances': [{
                    'InstanceId': 'i-12345',
                    'State': {'Name': 'running'},
                    'Tags': [{'Key': 'Environment', 'Value': 'staging'}]
                }, {
                    'InstanceId': 'i-67890',
                    'State': {'Name': 'terminated'},
                    'Tags': []
                }]
            }]
        }
        mock_describe.return_value = mock_response
        
        with patch.dict('os.environ', {'EXCLUDE_TAGS': '{}'}):
            instances = index.get_ec2_instances()
        
        # Should only return running instances
        self.assertEqual(len(instances), 1)
        self.assertEqual(instances[0]['id'], 'i-12345')
    
    def test_select_chaos_targets(self):
        """Test target selection logic."""
        all_resources = [
            {'id': 'i-1', 'type': 'ec2'},
            {'id': 'i-2', 'type': 'ec2'},
            {'id': 'i-3', 'type': 'ec2'},
            {'id': 'i-4', 'type': 'ec2'}
        ]
        
        # Should select up to max_chaos targets
        targets = index.select_chaos_targets(all_resources, 2)
        self.assertLessEqual(len(targets), 2)
        
        # Should return empty list for empty input
        empty_targets = index.select_chaos_targets([], 3)
        self.assertEqual(len(empty_targets), 0)
    
    @patch('index.ec2_client.terminate_instances')
    def test_terminate_ec2_instance(self, mock_terminate):
        """Test EC2 instance termination."""
        # Test dry run
        result = index.terminate_ec2_instance('i-12345', dry_run=True)
        self.assertTrue(result)
        mock_terminate.assert_not_called()
        
        # Test actual termination
        mock_terminate.return_value = {'TerminatingInstances': [{'InstanceId': 'i-12345'}]}
        result = index.terminate_ec2_instance('i-12345', dry_run=False)
        self.assertTrue(result)
        mock_terminate.assert_called_once_with(InstanceIds=['i-12345'])
    
    @patch('index.rds_client.delete_db_instance')
    def test_delete_rds_instance(self, mock_delete):
        """Test RDS instance deletion."""
        # Test dry run
        result = index.delete_rds_instance('db-test', dry_run=True)
        self.assertTrue(result)
        mock_delete.assert_not_called()
        
        # Test actual deletion
        mock_delete.return_value = {'DBInstance': {'DBInstanceIdentifier': 'db-test'}}
        result = index.delete_rds_instance('db-test', dry_run=False)
        self.assertTrue(result)
        mock_delete.assert_called_once_with(
            DBInstanceIdentifier='db-test',
            SkipFinalSnapshot=True,
            DeleteAutomatedBackups=True
        )
    
    @patch('index.elasticache_client.delete_cache_cluster')
    def test_delete_elasticache_cluster(self, mock_delete):
        """Test ElastiCache cluster deletion."""
        # Test dry run
        result = index.delete_elasticache_cluster('cluster-test', dry_run=True)
        self.assertTrue(result)
        mock_delete.assert_not_called()
        
        # Test actual deletion
        mock_delete.return_value = {'CacheCluster': {'CacheClusterId': 'cluster-test'}}
        result = index.delete_elasticache_cluster('cluster-test', dry_run=False)
        self.assertTrue(result)
        mock_delete.assert_called_once_with(CacheClusterId='cluster-test')
    
    @patch('index.sns_client')
    def test_send_notification(self, mock_sns):
        """Test SNS notification sending."""
        mock_sns.publish.return_value = {'MessageId': 'test-id'}
        
        # Mock environment with SNS topic ARN
        with patch.dict('os.environ', {'SNS_TOPIC_ARN': 'arn:aws:sns:us-east-1:123456789012:test-topic'}):
            index.send_notification('Test message')
        
        mock_sns.publish.assert_called_once()
    
    @patch('index.get_resource_types')
    @patch('index.get_ec2_instances')
    @patch('index.get_rds_instances')
    @patch('index.get_elasticache_clusters')
    @patch('index.select_chaos_targets')
    @patch('index.terminate_ec2_instance')
    @patch('index.delete_rds_instance')
    @patch('index.delete_elasticache_cluster')
    @patch('index.send_notification')
    def test_lambda_handler(self, mock_notify, mock_delete_ec, mock_delete_rds, mock_delete_elasticache, mock_select, mock_get_ec, mock_get_rds, mock_get_elasticache, mock_get_types):
        """Test the main Lambda handler."""
        # Setup mocks
        mock_get_types.return_value = ['ec2']
        mock_get_ec.return_value = [{'id': 'i-12345', 'type': 'ec2', 'state': 'running', 'tags': []}]
        mock_get_rds.return_value = []
        mock_get_elasticache.return_value = []
        mock_select.return_value = [{'id': 'i-12345', 'type': 'ec2', 'state': 'running', 'tags': []}]
        mock_delete_ec.return_value = True
        
        # Mock environment variables
        with patch.dict('os.environ', {
            'RESOURCE_TYPES': 'ec2',
            'EXCLUDE_TAGS': '{}',
            'MAX_CHAOS_PER_RUN': '1',
            'DRY_RUN': 'true',
            'AWS_REGION': 'us-east-1',
            'ENABLED': 'true'
        }):
            result = index.lambda_handler({}, {})
        
        # Verify result
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['chaos_executed'], 1)
        self.assertEqual(len(body['results']), 1)
        self.assertTrue(body['results'][0]['success'])
    
    def test_lambda_handler_disabled(self):
        """Test Lambda handler when disabled."""
        with patch.dict('os.environ', {'ENABLED': 'false'}):
            result = index.lambda_handler({}, {})
        
        self.assertEqual(result['statusCode'], 200)
        body = json.loads(result['body'])
        self.assertEqual(body['message'], 'Chaos Monkey is disabled')


if __name__ == '__main__':
    unittest.main()
