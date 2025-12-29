import unittest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.main import (
    DockerHealthChecker, ContainerMetrics, HealthStatus, 
    AlertConfig, MonitoringConfig, NotificationConfig, AppConfig
)


class TestDockerHealthChecker(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.alert_config = AlertConfig(
            cpu_threshold=80.0,
            memory_threshold=85.0,
            disk_threshold=90.0,
            network_threshold=1000.0
        )
        
        self.monitoring_config = MonitoringConfig(
            interval=5,
            containers=['test-container']
        )
        
        self.notification_config = NotificationConfig(
            console=True,
            file='test_alerts.log'
        )
        
        self.config = AppConfig(
            monitoring=self.monitoring_config,
            alerts=self.alert_config,
            notifications=self.notification_config
        )
        
        self.checker = DockerHealthChecker(self.config)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists('test_alerts.log'):
            os.remove('test_alerts.log')
    
    @patch('subprocess.run')
    def test_get_container_list(self, mock_run):
        """Test getting list of containers"""
        mock_run.return_value = MagicMock(
            stdout='container1\ncontainer2\ncontainer3\n',
            stderr='',
            returncode=0
        )
        
        containers = self.checker.get_container_list()
        self.assertEqual(containers, ['container1', 'container2', 'container3'])
    
    @patch('subprocess.run')
    def test_get_container_stats(self, mock_run):
        """Test getting container statistics"""
        mock_stats = {
            'CPUPerc': '12.50%',
            'MemUsage': '256.00MiB / 1024.00MiB',
            'MemPerc': '25.00%',
            'NetIO': '100.00MB / 50.00MB',
            'BlockIO': '10.00MB / 5.00MB'
        }
        
        mock_run.return_value = MagicMock(
            stdout=json.dumps(mock_stats),
            stderr='',
            returncode=0
        )
        
        metrics = self.checker.get_container_stats('test-container')
        
        self.assertIsNotNone(metrics)
        self.assertEqual(metrics.name, 'test-container')
        self.assertEqual(metrics.cpu_percent, 12.5)
        self.assertEqual(metrics.memory_usage, 256.0)
        self.assertEqual(metrics.memory_limit, 1024.0)
        self.assertEqual(metrics.memory_percent, 25.0)
        self.assertEqual(metrics.network_rx, 100.0)
        self.assertEqual(metrics.network_tx, 50.0)
        self.assertEqual(metrics.disk_read, 10.0)
        self.assertEqual(metrics.disk_write, 5.0)
        self.assertEqual(metrics.status, HealthStatus.HEALTHY)
    
    def test_parse_memory_value(self):
        """Test memory value parsing"""
        self.assertEqual(self.checker.parse_memory_value('100.00MiB'), 100.0)
        self.assertEqual(self.checker.parse_memory_value('1.5GiB'), 1536.0)  # 1.5 * 1024
        self.assertEqual(self.checker.parse_memory_value('512.0KiB'), 0.5)   # 512 / 1024
        self.assertEqual(self.checker.parse_memory_value('1024B'), 0.001)    # 1024 / (1024*1024)
        self.assertEqual(self.checker.parse_memory_value('invalid'), 0.0)
    
    def test_calculate_health_status(self):
        """Test health status calculation"""
        # Healthy status
        status = self.checker.calculate_health_status(50.0, 50.0, 10.0, 100.0)
        self.assertEqual(status, HealthStatus.HEALTHY)
        
        # Warning status
        status = self.checker.calculate_health_status(65.0, 70.0, 10.0, 100.0)  # CPU > 64%
        self.assertEqual(status, HealthStatus.WARNING)
        
        # Critical status
        status = self.checker.calculate_health_status(85.0, 50.0, 10.0, 100.0)  # CPU > 80%
        self.assertEqual(status, HealthStatus.CRITICAL)
    
    def test_check_alerts(self):
        """Test alert checking and notification"""
        metrics = ContainerMetrics(
            name='test-container',
            cpu_percent=85.0,  # Above threshold
            memory_usage=500.0,
            memory_limit=1000.0,
            memory_percent=50.0,
            disk_read=10.0,
            disk_write=5.0,
            network_rx=100.0,
            network_tx=50.0,
            status=HealthStatus.CRITICAL,
            timestamp=datetime.now()
        )
        
        initial_alert_count = len(self.checker.alert_history)
        self.checker.check_alerts(metrics)
        
        # Should have added an alert
        self.assertEqual(len(self.checker.alert_history), initial_alert_count + 1)
        
        alert_data = self.checker.alert_history[-1]
        self.assertEqual(alert_data['container'], 'test-container')
        self.assertEqual(alert_data['status'], '🔴')
        self.assertIn('High CPU usage', alert_data['alerts'][0])
    
    def test_generate_recommendations(self):
        """Test recommendation generation"""
        # Create some test metrics
        metrics1 = ContainerMetrics(
            name='test', cpu_percent=95.0, memory_usage=800.0, memory_limit=1000.0,
            memory_percent=80.0, disk_read=10.0, disk_write=5.0,
            network_rx=100.0, network_tx=50.0, status=HealthStatus.CRITICAL,
            timestamp=datetime.now()
        )
        
        metrics2 = ContainerMetrics(
            name='test', cpu_percent=50.0, memory_usage=400.0, memory_limit=1000.0,
            memory_percent=40.0, disk_read=5.0, disk_write=2.0,
            network_rx=50.0, network_tx=25.0, status=HealthStatus.HEALTHY,
            timestamp=datetime.now()
        )
        
        history = [metrics1, metrics2]
        recommendations = self.checker.generate_recommendations(history)
        
        self.assertTrue(any('CPU' in rec for rec in recommendations))
    
    def test_generate_health_report(self):
        """Test health report generation"""
        # Add some test data to metrics history
        metrics = ContainerMetrics(
            name='test-container',
            cpu_percent=50.0,
            memory_usage=500.0,
            memory_limit=1000.0,
            memory_percent=50.0,
            disk_read=10.0,
            disk_write=5.0,
            network_rx=100.0,
            network_tx=50.0,
            status=HealthStatus.HEALTHY,
            timestamp=datetime.now()
        )
        
        self.checker.metrics_history['test-container'] = [metrics]
        
        report = self.checker.generate_health_report()
        
        self.assertIn('timestamp', report)
        self.assertIn('summary', report)
        self.assertIn('containers', report)
        self.assertIn('alerts', report)
        
        self.assertEqual(report['summary']['total_containers'], 1)
        self.assertEqual(report['summary']['healthy_containers'], 1)
        self.assertEqual(report['summary']['critical_containers'], 0)
        self.assertEqual(report['summary']['overall_health'], 'HEALTHY')
    
    @patch('builtins.open')
    @patch('yaml.safe_load')
    def test_load_config(self, mock_yaml_load, mock_open):
        """Test configuration loading"""
        mock_config = {
            'monitoring': {'interval': 10, 'containers': ['web', 'db']},
            'alerts': {'cpu_threshold': 90, 'memory_threshold': 95},
            'notifications': {'console': True, 'file': 'alerts.log'}
        }
        mock_yaml_load.return_value = mock_config
        
        config = load_config('test_config.yaml')
        
        self.assertEqual(config.monitoring.interval, 10)
        self.assertEqual(config.monitoring.containers, ['web', 'db'])
        self.assertEqual(config.alerts.cpu_threshold, 90)
        self.assertEqual(config.alerts.memory_threshold, 95)
        self.assertTrue(config.notifications.console)
        self.assertEqual(config.notifications.file, 'alerts.log')


def load_config(config_path: str):
    """Mock load_config function for testing"""
    from src.main import AppConfig, MonitoringConfig, AlertConfig, NotificationConfig
    import yaml
    
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        monitoring = MonitoringConfig(**config_data.get('monitoring', {}))
        alerts = AlertConfig(**config_data.get('alerts', {}))
        notifications = NotificationConfig(**config_data.get('notifications', {}))
        
        return AppConfig(
            monitoring=monitoring,
            alerts=alerts,
            notifications=notifications
        )
    except Exception as e:
        print(f"Error loading config: {e}")
        print("Using default configuration...")
        return AppConfig(
            monitoring=MonitoringConfig(),
            alerts=AlertConfig(),
            notifications=NotificationConfig()
        )


if __name__ == '__main__':
    unittest.main()
