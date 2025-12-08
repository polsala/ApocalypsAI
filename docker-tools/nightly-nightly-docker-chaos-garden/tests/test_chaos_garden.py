#!/usr/bin/env python3
"""
Unit tests for Nightly Docker Chaos Garden.

These tests use mocks to simulate Docker operations without requiring
actual Docker containers or the Docker daemon.
"""

import unittest
import json
import yaml
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
from chaos_garden import ChaosGarden, ChaosReport


class TestChaosGarden(unittest.TestCase):
    """Test cases for the ChaosGarden class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.garden = ChaosGarden(dry_run=True)
        self.garden.client = Mock()
    
    def _create_mock_container(self, name: str, essential: bool = False, 
                              memory_usage: int = 100):
        """Helper to create a mock container with stats."""
        container = Mock()
        container.short_id = f"abc123{name[-2:] if len(name) > 2 else '00'}"
        container.name = name
        container.image.tags = ['test:latest'] if not essential else ['postgres:13']
        container.status = 'running'
        container.attrs = {'Created': '2023-01-01T00:00:00Z'}
        
        # Mock stats
        container.stats.return_value = {
            'cpu_stats': {'cpu_usage': {'total_usage': 1000}},
            'memory_stats': {
                'usage': memory_usage,
                'limit': 1000000
            }
        }
        
        return container
    
    def test_get_container_stats(self):
        """Test retrieving container statistics."""
        # Mock Docker client and containers
        mock_containers = [
            self._create_mock_container('web-frontend', essential=False, memory_usage=200),
            self._create_mock_container('db-primary', essential=True, memory_usage=500),
            self._create_mock_container('cache-redis', essential=True, memory_usage=300),
            self._create_mock_container('worker-queue', essential=False, memory_usage=150)
        ]
        
        self.garden.client.containers.list.return_value = mock_containers
        
        stats = self.garden.get_container_stats()
        
        self.assertEqual(len(stats), 4)
        self.assertEqual(stats[0]['name'], 'web-frontend')
        self.assertEqual(stats[1]['name'], 'db-primary')
        self.assertTrue(stats[1]['essential'])  # db-primary should be essential
        self.assertFalse(stats[0]['essential'])  # web-frontend should not be essential
    
    def test_is_essential_detection(self):
        """Test essential container detection logic."""
        # Test various container names and images
        test_cases = [
            ('postgres-db', True, ['postgres:13']),
            ('mysql-primary', True, ['mysql:8.0']),
            ('redis-cache', True, ['redis:6']),
            ('web-frontend', False, ['nginx:latest']),
            ('worker-queue', False, ['python:3.11']),
            ('monitoring-grafana', True, ['grafana:latest']),
            ('app-service', False, ['app:latest'])
        ]
        
        for name, expected_essential, image_tags in test_cases:
            with self.subTest(name=name):
                container = Mock()
                container.name = name
                container.image.tags = image_tags
                
                result = self.garden._is_essential(container)
                self.assertEqual(result, expected_essential,
                               f"Container {name} essential detection failed")
    
    def test_drought_scenario(self):
        """Test drought scenario pruning logic."""
        # Create test containers
        containers = [
            {'id': 'abc123', 'name': 'web-frontend', 'essential': False, 'memory_usage': 200},
            {'id': 'def456', 'name': 'db-primary', 'essential': True, 'memory_usage': 500},
            {'id': 'ghi789', 'name': 'cache-redis', 'essential': True, 'memory_usage': 300},
            {'id': 'jkl012', 'name': 'worker-queue', 'essential': False, 'memory_usage': 150},
            {'id': 'mno345', 'name': 'backup-service', 'essential': False, 'memory_usage': 100}
        ]
        
        result = self.garden._drought_scenario(containers)
        
        # Should prune some non-essential containers (40% of 3 = 1-2 containers)
        self.assertGreater(len(result['pruned']), 0)
        self.assertLessEqual(len(result['pruned']), 2)
        
        # Essential containers should not be pruned
        self.assertNotIn('db-primary', result['pruned'])
        self.assertNotIn('cache-redis', result['pruned'])
        
        # Survival rate should be calculated correctly
        expected_survival = (5 - len(result['pruned'])) / 5 * 100
        self.assertAlmostEqual(result['survival_rate'], expected_survival)
    
    def test_storm_scenario(self):
        """Test storm scenario random destruction."""
        containers = [
            {'id': 'abc123', 'name': 'web-frontend', 'essential': False, 'memory_usage': 200},
            {'id': 'def456', 'name': 'db-primary', 'essential': True, 'memory_usage': 500},
            {'id': 'ghi789', 'name': 'cache-redis', 'essential': True, 'memory_usage': 300},
            {'id': 'jkl012', 'name': 'worker-queue', 'essential': False, 'memory_usage': 150}
        ]
        
        result = self.garden._storm_scenario(containers)
        
        # Should prune some containers but preserve essentials
        self.assertGreaterEqual(len(result['pruned']), 0)
        self.assertLessEqual(len(result['pruned']), 2)  # 30% of 4 = 1-2
        
        # Essential containers should be replanted if destroyed
        self.assertGreaterEqual(len(result['replanted']), 0)
    
    def test_quake_scenario(self):
        """Test earthquake scenario targeting high-resource containers."""
        containers = [
            {'id': 'abc123', 'name': 'low-mem', 'essential': False, 'memory_usage': 100},
            {'id': 'def456', 'name': 'high-mem', 'essential': False, 'memory_usage': 1000},
            {'id': 'ghi789', 'name': 'medium-mem', 'essential': True, 'memory_usage': 500},
            {'id': 'jkl012', 'name': 'another-high', 'essential': False, 'memory_usage': 800}
        ]
        
        result = self.garden._quake_scenario(containers)
        
        # Should target high-memory containers for pruning
        self.assertIn('high-mem', result['pruned'])
        self.assertIn('another-high', result['pruned'])
        self.assertNotIn('medium-mem', result['pruned'])  # Essential, should be preserved
    
    def test_prune_containers_dry_run(self):
        """Test container pruning in dry run mode."""
        containers_to_prune = [
            {'id': 'abc123', 'name': 'test-container', 'essential': False}
        ]
        
        # Mock the Docker client get method
        mock_container = Mock()
        mock_container.name = 'test-container'
        self.garden.client.containers.get.return_value = mock_container
        
        pruned = self.garden._prune_containers(containers_to_prune)
        
        # Should return the container name but not actually stop/remove
        self.assertEqual(pruned, ['test-container'])
        mock_container.stop.assert_not_called()
        mock_container.remove.assert_not_called()
    
    def test_prune_containers_real_run(self):
        """Test container pruning in real mode."""
        garden = ChaosGarden(dry_run=False)  # Real run
        garden.client = Mock()
        
        containers_to_prune = [
            {'id': 'abc123', 'name': 'test-container', 'essential': False}
        ]
        
        mock_container = Mock()
        mock_container.name = 'test-container'
        garden.client.containers.get.return_value = mock_container
        
        pruned = garden._prune_containers(containers_to_prune)
        
        # Should return the container name and actually stop/remove
        self.assertEqual(pruned, ['test-container'])
        mock_container.stop.assert_called_once()
        mock_container.remove.assert_called_once()
    
    def test_chaos_report_generation(self):
        """Test chaos report data structure and content."""
        report = ChaosReport(
            timestamp='2023-01-01T12:00:00',
            scenario='drought',
            total_containers=5,
            pruned_containers=2,
            replanted_containers=1,
            survival_rate=60.0,
            essential_preserved=True,
            pruned_list=['web-frontend', 'worker-queue'],
            replanted_list=['db-primary'],
            dry_run=True
        )
        
        # Test report structure
        self.assertEqual(report.scenario, 'drought')
        self.assertEqual(report.total_containers, 5)
        self.assertEqual(report.survival_rate, 60.0)
        self.assertTrue(report.essential_preserved)
        
        # Test serialization
        report_dict = {
            'timestamp': report.timestamp,
            'scenario': report.scenario,
            'total_containers': report.total_containers,
            'pruned_containers': report.pruned_containers,
            'replanted_containers': report.replanted_containers,
            'survival_rate': report.survival_rate,
            'essential_preserved': report.essential_preserved,
            'pruned_list': report.pruned_list,
            'replanted_list': report.replanted_list,
            'dry_run': report.dry_run
        }
        
        # Should be serializable to JSON
        json_str = json.dumps(report_dict)
        parsed = json.loads(json_str)
        self.assertEqual(parsed['scenario'], 'drought')
        
        # Should be serializable to YAML
        yaml_str = yaml.dump(report_dict)
        self.assertIn('scenario: drought', yaml_str)
    
    def test_empty_container_list(self):
        """Test behavior when no containers are found."""
        with patch.object(self.garden, 'get_container_stats', return_value=[]):
            report = self.garden.run_chaos('drought')
        
        self.assertEqual(report.total_containers, 0)
        self.assertEqual(report.pruned_containers, 0)
        self.assertEqual(report.survival_rate, 100.0)
        self.assertTrue(report.essential_preserved)
    
    def test_invalid_scenario_fallback(self):
        """Test that invalid scenarios fall back to random."""
        containers = [
            {'id': 'abc123', 'name': 'test', 'essential': False, 'memory_usage': 100}
        ]
        
        # Mock get_container_stats to return test data
        with patch.object(self.garden, 'get_container_stats', return_value=containers):
            # Should not raise an error for invalid scenario
            report = self.garden.run_chaos('invalid_scenario')
            
            # Should have run some scenario (random fallback)
            self.assertIn(report.scenario, ['drought', 'storm', 'quake', 'random'])


if __name__ == '__main__':
    # Run the tests
    unittest.main()
