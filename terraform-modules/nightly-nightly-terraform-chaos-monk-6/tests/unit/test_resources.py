import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add the parent directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chaos_lambda import (
    is_resource_protected,
    get_ec2_instances,
    get_rds_instances,
    get_ecs_services,
    terminate_ec2_instance,
    delete_rds_instance,
    update_ecs_service
)


class TestResources(unittest.TestCase):
    """Test resource management functions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_ec2 = MagicMock()
        self.mock_rds = MagicMock()
        self.mock_ecs = MagicMock()
    
    def test_is_resource_protected_with_excluded_tags(self):
        """Test resource protection with excluded tags"""
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
        
        # Test with no tags
        tags = []
        with patch.dict('os.environ', {'EXCLUDED_TAGS': json.dumps(excluded_tags)}):
            result = is_resource_protected(tags)
            self.assertFalse(result)
        
        # Test with None tags
        tags = None
        with patch.dict('os.environ', {'EXCLUDED_TAGS': json.dumps(excluded_tags)}):
            result = is_resource_protected(tags)
            self.assertFalse(result)
    
    @patch('src.chaos_lambda.ec2')
    def test_get_ec2_instances_success(self, mock_ec2_client):
        """Test successful EC2 instance retrieval"""
        # Mock successful response
        mock_ec2_client.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-1234567890abcdef0',
                            'State': {'Name': 'running'},
                            'Tags': [{'Key': 'Name', 'Value': 'test-instance'}]
                        },
                        {
                            'InstanceId': 'i-0987654321fedcba0',
                            'State': {'Name': 'stopped'},
                            'Tags': [{'Key': 'Name', 'Value': 'test-stopped'}]
                        }
                    ]
                }
            ]
        }
        
        instances = get_ec2_instances()
        
        self.assertEqual(len(instances), 2)
        self.assertEqual(instances[0]['id'], 'i-1234567890abcdef0')
        self.assertEqual(instances[0]['type'], 'aws_instance')
        self.assertEqual(instances[0]['state'], 'running')
        self.assertEqual(instances[0]['name'], 'test-instance')
        
        self.assertEqual(instances[1]['id'], 'i-0987654321fedcba0')
        self.assertEqual(instances[1]['type'], 'aws_instance')
        self.assertEqual(instances[1]['state'], 'stopped')
        self.assertEqual(instances[1]['name'], 'test-stopped')
    
    @patch('src.chaos_lambda.ec2')
    def test_get_ec2_instances_error(self, mock_ec2_client):
        """Test EC2 instance retrieval with error"""
        # Mock error response
        mock_ec2_client.describe_instances.side_effect = Exception("EC2 API Error")
        
        instances = get_ec2_instances()
        
        self.assertEqual(instances, [])
    
    @patch('src.chaos_lambda.ec2')
    def test_get_ec2_instances_empty(self, mock_ec2_client):
        """Test EC2 instance retrieval with empty response"""
        # Mock empty response
        mock_ec2_client.describe_instances.return_value = {'Reservations': []}
        
        instances = get_ec2_instances()
        
        self.assertEqual(instances, [])
    
    @patch('src.chaos_lambda.rds')
    def test_get_rds_instances_success(self, mock_rds_client):
        """Test successful RDS instance retrieval"""
        # Mock successful response
        mock_rds_client.describe_db_instances.return_value = {
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'test-db-1',
                    'DBInstanceStatus': 'available',
                    'TagList': [{'Key': 'Name', 'Value': 'test-db-1'}]
                },
                {
                    'DBInstanceIdentifier': 'test-db-2',
                    'DBInstanceStatus': 'available',
                    'TagList': [{'Key': 'Name', 'Value': 'test-db-2'}]
                }
            ]
        }
        
        instances = get_rds_instances()
        
        self.assertEqual(len(instances), 2)
        self.assertEqual(instances[0]['id'], 'test-db-1')
        self.assertEqual(instances[0]['type'], 'aws_rds_instance')
        self.assertEqual(instances[0]['state'], 'available')
        self.assertEqual(instances[0]['name'], 'test-db-1')
        
        self.assertEqual(instances[1]['id'], 'test-db-2')
        self.assertEqual(instances[1]['type'], 'aws_rds_instance')
        self.assertEqual(instances[1]['state'], 'available')
        self.assertEqual(instances[1]['name'], 'test-db-2')
    
    @patch('src.chaos_lambda.rds')
    def test_get_rds_instances_error(self, mock_rds_client):
        """Test RDS instance retrieval with error"""
        # Mock error response
        mock_rds_client.describe_db_instances.side_effect = Exception("RDS API Error")
        
        instances = get_rds_instances()
        
        self.assertEqual(instances, [])
    
    @patch('src.chaos_lambda.rds')
    def test_get_rds_instances_empty(self, mock_rds_client):
        """Test RDS instance retrieval with empty response"""
        # Mock empty response
        mock_rds_client.describe_db_instances.return_value = {'DBInstances': []}
        
        instances = get_rds_instances()
        
        self.assertEqual(instances, [])
    
    @patch('src.chaos_lambda.ecs')
    def test_get_ecs_services_success(self, mock_ecs_client):
        """Test successful ECS service retrieval"""
        # Mock successful responses
        mock_ecs_client.list_clusters.return_value = {
            'clusterArns': ['arn:aws:ecs:us-east-1:123456789012:cluster/test-cluster']
        }
        
        mock_ecs_client.list_services.return_value = {
            'serviceArns': ['arn:aws:ecs:us-east-1:123456789012:service/test-service']
        }
        
        mock_ecs_client.describe_services.return_value = {
            'services': [
                {
                    'serviceName': 'test-service',
                    'status': 'ACTIVE',
                    'tags': [{'Key': 'Name', 'Value': 'test-service'}],
                    'clusterArn': 'arn:aws:ecs:us-east-1:123456789012:cluster/test-cluster'
                }
            ]
        }
        
        services = get_ecs_services()
        
        self.assertEqual(len(services), 1)
        self.assertEqual(services[0]['id'], 'test-service')
        self.assertEqual(services[0]['type'], 'aws_ecs_service')
        self.assertEqual(services[0]['state'], 'ACTIVE')
        self.assertEqual(services[0]['name'], 'test-service')
    
    @patch('src.chaos_lambda.ecs')
    def test_get_ecs_services_error(self, mock_ecs_client):
        """Test ECS service retrieval with error"""
        # Mock error response
        mock_ecs_client.list_clusters.side_effect = Exception("ECS API Error")
        
        services = get_ecs_services()
        
        self.assertEqual(services, [])
    
    @patch('src.chaos_lambda.ecs')
    def test_get_ecs_services_empty(self, mock_ecs_client):
        """Test ECS service retrieval with empty response"""
        # Mock empty response
        mock_ecs_client.list_clusters.return_value = {'clusterArns': []}
        
        services = get_ecs_services()
        
        self.assertEqual(services, [])
    
    @patch('src.chaos_lambda.ec2')
    def test_terminate_ec2_instance_success(self, mock_ec2_client):
        """Test successful EC2 instance termination"""
        # Mock successful termination
        mock_ec2_client.terminate_instances.return_value = {
            'TerminatingInstances': [
                {
                    'InstanceId': 'i-1234567890abcdef0',
                    'CurrentState': {'Name': 'shutting-down'},
                    'PreviousState': {'Name': 'running'}
                }
            ]
        }
        
        with patch.dict('os.environ', {'SAFE_MODE': 'false'}):
            result = terminate_ec2_instance('i-1234567890abcdef0')
            self.assertTrue(result)
    
    @patch('src.chaos_lambda.ec2')
    def test_terminate_ec2_instance_error(self, mock_ec2_client):
        """Test EC2 instance termination with error"""
        # Mock error response
        mock_ec2_client.terminate_instances.side_effect = Exception("EC2 Termination Error")
        
        with patch.dict('os.environ', {'SAFE_MODE': 'false'}):
            result = terminate_ec2_instance('i-1234567890abcdef0')
            self.assertFalse(result)
    
    @patch('src.chaos_lambda.ec2')
    def test_terminate_ec2_instance_safe_mode(self, mock_ec2_client):
        """Test EC2 instance termination in safe mode"""
        with patch.dict('os.environ', {'SAFE_MODE': 'true'}):
            result = terminate_ec2_instance('i-1234567890abcdef0')
            self.assertTrue(result)
            # Should not call actual termination
            mock_ec2_client.terminate_instances.assert_not_called()
    
    @patch('src.chaos_lambda.rds')
    def test_delete_rds_instance_success(self, mock_rds_client):
        """Test successful RDS instance deletion"""
        # Mock successful deletion
        mock_rds_client.delete_db_instance.return_value = {
            'DBInstance': {
                'DBInstanceIdentifier': 'test-db',
                'DBInstanceStatus': 'deleting'
            }
        }
        
        with patch.dict('os.environ', {'SAFE_MODE': 'false'}):
            result = delete_rds_instance('test-db')
            self.assertTrue(result)
    
    @patch('src.chaos_lambda.rds')
    def test_delete_rds_instance_error(self, mock_rds_client):
        """Test RDS instance deletion with error"""
        # Mock error response
        mock_rds_client.delete_db_instance.side_effect = Exception("RDS Deletion Error")
        
        with patch.dict('os.environ', {'SAFE_MODE': 'false'}):
            result = delete_rds_instance('test-db')
            self.assertFalse(result)
    
    @patch('src.chaos_lambda.rds')
    def test_delete_rds_instance_safe_mode(self, mock_rds_client):
        """Test RDS instance deletion in safe mode"""
        with patch.dict('os.environ', {'SAFE_MODE': 'true'}):
            result = delete_rds_instance('test-db')
            self.assertTrue(result)
            # Should not call actual deletion
            mock_rds_client.delete_db_instance.assert_not_called()
    
    @patch('src.chaos_lambda.ecs')
    def test_update_ecs_service_success(self, mock_ecs_client):
        """Test successful ECS service update"""
        # Mock successful update
        mock_ecs_client.update_service.return_value = {
            'service': {
                'serviceName': 'test-service',
                'desiredCount': 0,
                'status': 'ACTIVE'
            }
        }
        
        with patch.dict('os.environ', {'SAFE_MODE': 'false'}):
            result = update_ecs_service('test-service', 'arn:aws:ecs:us-east-1:123456789012:cluster/test-cluster')
            self.assertTrue(result)
    
    @patch('src.chaos_lambda.ecs')
    def test_update_ecs_service_error(self, mock_ecs_client):
        """Test ECS service update with error"""
        # Mock error response
        mock_ecs_client.update_service.side_effect = Exception("ECS Update Error")
        
        with patch.dict('os.environ', {'SAFE_MODE': 'false'}):
            result = update_ecs_service('test-service', 'arn:aws:ecs:us-east-1:123456789012:cluster/test-cluster')
            self.assertFalse(result)
    
    @patch('src.chaos_lambda.ecs')
    def test_update_ecs_service_safe_mode(self, mock_ecs_client):
        """Test ECS service update in safe mode"""
        with patch.dict('os.environ', {'SAFE_MODE': 'true'}):
            result = update_ecs_service('test-service', 'arn:aws:ecs:us-east-1:123456789012:cluster/test-cluster')
            self.assertTrue(result)
            # Should not call actual update
            mock_ecs_client.update_service.assert_not_called()


if __name__ == '__main__':
    unittest.main()
