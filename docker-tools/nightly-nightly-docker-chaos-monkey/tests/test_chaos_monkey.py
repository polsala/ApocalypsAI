import unittest
from unittest.mock import Mock, patch, MagicMock
import docker
from src.chaos_monkey import ChaosMonkey, ChaosConfig, ChaosEvent


class TestChaosMonkey(unittest.TestCase):
    """Test cases for ChaosMonkey class."""
    
    def setUp(self):
        """Setup test environment."""
        self.config = ChaosConfig(
            duration=60,
            intensity='medium',
            interval=10,
            target_label='chaos.monkey=true',
            dry_run=True
        )
        self.chaos_monkey = ChaosMonkey(self.config)
        self.chaos_monkey.docker_client = Mock()
    
    def test_get_target_containers(self):
        """Test getting target containers."""
        # Mock containers
        container1 = Mock()
        container1.name = 'test-app'
        container1.labels = {'chaos.monkey': 'true'}
        
        container2 = Mock()
        container2.name = 'other-app'
        container2.labels = {'chaos.monkey': 'false'}
        
        container3 = Mock()
        container3.name = 'chaos-monkey'
        container3.labels = {'chaos.monkey': 'true'}
        
        self.chaos_monkey.docker_client.containers.list.return_value = [
            container1, container2, container3
        ]
        
        target_containers = self.chaos_monkey._get_target_containers()
        
        # Should only return container1 (not container2 due to label, not container3 due to name)
        self.assertEqual(len(target_containers), 1)
        self.assertEqual(target_containers[0].name, 'test-app')
    
    def test_get_intensity_multiplier(self):
        """Test intensity multiplier calculation."""
        self.config.intensity = 'low'
        self.assertEqual(self.chaos_monkey._get_intensity_multiplier(), 0.3)
        
        self.config.intensity = 'medium'
        self.assertEqual(self.chaos_monkey._get_intensity_multiplier(), 0.6)
        
        self.config.intensity = 'high'
        self.assertEqual(self.chaos_monkey._get_intensity_multiplier(), 1.0)
    
    def test_kill_container_dry_run(self):
        """Test container kill in dry run mode."""
        container = Mock()
        container.name = 'test-container'
        
        with patch('src.chaos_monkey.logging.getLogger') as mock_logger:
            result = self.chaos_monkey._kill_container(container)
            
            self.assertTrue(result)
            container.kill.assert_not_called()
            mock_logger.return_value.info.assert_called()
    
    def test_should_stop_duration(self):
        """Test stopping based on duration."""
        self.config.duration = 1
        self.chaos_monkey.running = True
        self.chaos_monkey.start_time = time.time() - 2  # 2 seconds ago
        
        self.assertTrue(self.chaos_monkey._should_stop())
    
    def test_should_stop_infinite(self):
        """Test infinite duration."""
        self.config.duration = 0
        self.chaos_monkey.running = True
        self.chaos_monkey.start_time = time.time() - 100  # 100 seconds ago
        
        self.assertFalse(self.chaos_monkey._should_stop())
    
    def test_should_stop_not_running(self):
        """Test stopping when not running."""
        self.chaos_monkey.running = False
        
        self.assertTrue(self.chaos_monkey._should_stop())
    
    def test_record_event(self):
        """Test recording chaos events."""
        event = ChaosEvent(
            timestamp='2024-01-01T00:00:00Z',
            event_type='test_event',
            target='test-container',
            intensity='medium',
            success=True,
            details={}
        )
        
        self.chaos_monkey._record_event(event)
        
        self.assertEqual(len(self.chaos_monkey.events), 1)
        self.assertEqual(self.chaos_monkey.events[0], event)
    
    def test_get_stats(self):
        """Test getting chaos monkey statistics."""
        # Add some test events
        event1 = ChaosEvent(
            timestamp='2024-01-01T00:00:00Z',
            event_type='container_kill',
            target='test-container',
            intensity='medium',
            success=True,
            details={}
        )
        
        event2 = ChaosEvent(
            timestamp='2024-01-01T00:01:00Z',
            event_type='cpu_spike',
            target='test-container',
            intensity='medium',
            success=False,
            details={}
        )
        
        self.chaos_monkey.events = [event1, event2]
        self.chaos_monkey.running = True
        self.chaos_monkey.start_time = time.time() - 10
        
        stats = self.chaos_monkey.get_stats()
        
        self.assertEqual(stats['total_events'], 2)
        self.assertEqual(stats['successful_events'], 1)
        self.assertEqual(stats['failed_events'], 1)
        self.assertEqual(stats['success_rate'], 0.5)
        self.assertEqual(stats['event_types']['container_kill'], 1)
        self.assertEqual(stats['event_types']['cpu_spike'], 1)
        self.assertTrue(stats['running'])


if __name__ == '__main__':
    import time
    unittest.main()
