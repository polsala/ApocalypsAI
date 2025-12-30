"""Tests for the RollbackManager class."""

import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock

from src.rollback import RollbackManager


class TestRollbackManager(unittest.TestCase):
    """Test cases for RollbackManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.snapshot_dir = os.path.join(self.temp_dir, 'snapshots')
        self.rollback_manager = RollbackManager(self.snapshot_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_create_snapshot(self):
        """Test creating a snapshot."""
        inventory_path = os.path.join(self.temp_dir, 'test_inventory.ini')
        with open(inventory_path, 'w') as f:
            f.write('[all]\nlocalhost\n')
        
        snapshot_id = self.rollback_manager.create_snapshot(inventory_path, 'Test snapshot')
        
        self.assertTrue(snapshot_id.startswith('snapshot_'))
        
        # Check that snapshot file was created
        snapshot_file = os.path.join(self.snapshot_dir, f'{snapshot_id}.json')
        self.assertTrue(os.path.exists(snapshot_file))
        
        # Check snapshot content
        with open(snapshot_file, 'r') as f:
            snapshot_data = json.load(f)
        
        self.assertEqual(snapshot_data['description'], 'Test snapshot')
        self.assertEqual(snapshot_data['inventory'], inventory_path)
        self.assertIn('timestamp', snapshot_data)
    
    @patch('subprocess.run')
    def test_rollback_to_snapshot_success(self, mock_run):
        """Test successful rollback to snapshot."""
        # Create a snapshot
        inventory_path = os.path.join(self.temp_dir, 'test_inventory.ini')
        with open(inventory_path, 'w') as f:
            f.write('[all]\nlocalhost\n')
        
        snapshot_id = self.rollback_manager.create_snapshot(inventory_path, 'Test snapshot')
        
        # Mock successful subprocess run
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'PLAY [all] ***\nok: [localhost]\n'
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        # Mock file operations
        with patch('builtins.open', unittest.mock.mock_open(read_data='test playbook content')):
            with patch('os.path.exists', return_value=True):
                with patch('os.remove'):
                    result = self.rollback_manager.rollback_to_snapshot(snapshot_id, inventory_path)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['snapshot_id'], snapshot_id)
    
    def test_rollback_to_snapshot_not_found(self):
        """Test rollback to non-existent snapshot."""
        inventory_path = os.path.join(self.temp_dir, 'test_inventory.ini')
        result = self.rollback_manager.rollback_to_snapshot('nonexistent_snapshot', inventory_path)
        
        self.assertFalse(result['success'])
        self.assertIn('not found', result['error'])
    
    def test_list_snapshots(self):
        """Test listing snapshots."""
        # Create some snapshots
        inventory_path = os.path.join(self.temp_dir, 'test_inventory.ini')
        with open(inventory_path, 'w') as f:
            f.write('[all]\nlocalhost\n')
        
        snapshot_ids = []
        for i in range(3):
            snapshot_id = self.rollback_manager.create_snapshot(inventory_path, f'Test snapshot {i}')
            snapshot_ids.append(snapshot_id)
        
        snapshots = self.rollback_manager.list_snapshots()
        
        self.assertEqual(len(snapshots), 3)
        self.assertEqual(snapshots[0]['description'], 'Test snapshot 2')  # Should be sorted by timestamp
        self.assertEqual(snapshots[1]['description'], 'Test snapshot 1')
        self.assertEqual(snapshots[2]['description'], 'Test snapshot 0')
    
    def test_cleanup_old_snapshots(self):
        """Test cleaning up old snapshots."""
        # Create more than 10 snapshots
        inventory_path = os.path.join(self.temp_dir, 'test_inventory.ini')
        with open(inventory_path, 'w') as f:
            f.write('[all]\nlocalhost\n')
        
        for i in range(15):
            self.rollback_manager.create_snapshot(inventory_path, f'Test snapshot {i}')
        
        # Clean up old snapshots
        self.rollback_manager.cleanup_old_snapshots(keep_count=10)
        
        snapshots = self.rollback_manager.list_snapshots()
        self.assertEqual(len(snapshots), 10)


if __name__ == '__main__':
    unittest.main()
