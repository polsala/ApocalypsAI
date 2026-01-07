import unittest
from unittest.mock import Mock, patch
from health_check import app


class TestHealthCheck(unittest.TestCase):
    """Test cases for health check endpoints."""
    
    def setUp(self):
        """Setup test client."""
        self.app = app.test_client()
        self.app.testing = True
    
    @patch('health_check.docker_client')
    def test_health_endpoint_healthy(self, mock_docker):
        """Test health endpoint when healthy."""
        mock_docker.ping.return_value = True
        
        response = self.app.get('/health')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertTrue(data['docker_connected'])
    
    @patch('health_check.docker_client')
    def test_health_endpoint_unhealthy(self, mock_docker):
        """Test health endpoint when unhealthy."""
        mock_docker.ping.side_effect = Exception('Docker connection failed')
        
        response = self.app.get('/health')
        
        self.assertEqual(response.status_code, 503)
        data = response.get_json()
        self.assertEqual(data['status'], 'unhealthy')
        self.assertFalse(data['docker_connected'])
    
    @patch('health_check.docker_client')
    def test_ready_endpoint_ready(self, mock_docker):
        """Test ready endpoint when ready."""
        mock_docker.containers.list.return_value = [Mock(), Mock()]
        
        response = self.app.get('/ready')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ready')
        self.assertEqual(data['containers_count'], 2)
    
    @patch('health_check.docker_client')
    def test_ready_endpoint_not_ready(self, mock_docker):
        """Test ready endpoint when not ready."""
        mock_docker.containers.list.side_effect = Exception('Cannot list containers')
        
        response = self.app.get('/ready')
        
        self.assertEqual(response.status_code, 503)
        data = response.get_json()
        self.assertEqual(data['status'], 'not ready')


if __name__ == '__main__':
    unittest.main()
