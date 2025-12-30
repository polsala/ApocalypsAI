"""Rollback functionality for failed playbook executions."""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class RollbackManager:
    """Handle rollback operations for failed playbook executions."""
    
    def __init__(self, snapshot_dir: str = 'snapshots'):
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(exist_ok=True)
    
    def create_snapshot(self, inventory_path: str, description: str = "") -> str:
        """Create a snapshot of the current system state."""
        snapshot_id = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snapshot_file = self.snapshot_dir / f"{snapshot_id}.json"
        
        snapshot_data = {
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'inventory': inventory_path,
            'hosts': {}
        }
        
        # Get current state of hosts
        try:
            result = subprocess.run(
                ['ansible', '-i', inventory_path, 'all', '-m', 'setup'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Parse ansible setup output
                # This is a simplified version - in practice you'd want more sophisticated parsing
                snapshot_data['hosts'] = {
                    'ansible_facts': 'captured',
                    'stdout': result.stdout
                }
            else:
                snapshot_data['error'] = f"Failed to capture snapshot: {result.stderr}"
        except Exception as e:
            snapshot_data['error'] = f"Exception during snapshot: {str(e)}"
        
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot_data, f, indent=2)
        
        return snapshot_id
    
    def rollback_to_snapshot(self, snapshot_id: str, inventory_path: str) -> Dict[str, any]:
        """Rollback to a specific snapshot."""
        snapshot_file = self.snapshot_dir / f"{snapshot_id}.json"
        
        if not snapshot_file.exists():
            return {
                'success': False,
                'error': f"Snapshot {snapshot_id} not found"
            }
        
        try:
            with open(snapshot_file, 'r') as f:
                snapshot_data = json.load(f)
            
            # Create rollback playbook
            rollback_playbook = self._generate_rollback_playbook(snapshot_data, inventory_path)
            
            # Execute rollback
            result = subprocess.run(
                ['ansible-playbook', rollback_playbook, '-i', inventory_path],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            rollback_result = {
                'success': result.returncode == 0,
                'snapshot_id': snapshot_id,
                'execution_time': 0,  # Would need to track this
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            # Clean up temporary rollback playbook
            if os.path.exists(rollback_playbook):
                os.remove(rollback_playbook)
            
            return rollback_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Rollback failed: {str(e)}"
            }
    
    def _generate_rollback_playbook(self, snapshot_data: Dict, inventory_path: str) -> str:
        """Generate a rollback playbook based on snapshot data."""
        playbook_content = [
            {
                'name': f"Rollback to snapshot {snapshot_data.get('timestamp', '')}",
                'hosts': 'all',
                'become': True,
                'tasks': [
                    {
                        'name': 'Ensure rollback is logged',
                        'debug': {
                            'msg': f"Rolling back to snapshot created at {snapshot_data.get('timestamp', '')}"
                        }
                    }
                ]
            }
        ]
        
        # Add specific rollback tasks based on snapshot data
        # This is a simplified example - real implementation would be more complex
        if 'error' in snapshot_data:
            playbook_content[0]['tasks'].append({
                'name': 'Handle snapshot error',
                'debug': {
                    'msg': f"Snapshot had error: {snapshot_data['error']}"
                }
            })
        
        # Write playbook to temporary file
        playbook_file = f"rollback_{int(time.time())}.yml"
        with open(playbook_file, 'w') as f:
            import yaml
            yaml.dump(playbook_content, f, default_flow_style=False)
        
        return playbook_file
    
    def list_snapshots(self) -> List[Dict[str, any]]:
        """List all available snapshots."""
        snapshots = []
        
        for snapshot_file in self.snapshot_dir.glob('*.json'):
            try:
                with open(snapshot_file, 'r') as f:
                    snapshot_data = json.load(f)
                    snapshots.append({
                        'id': snapshot_file.stem,
                        'timestamp': snapshot_data.get('timestamp'),
                        'description': snapshot_data.get('description', ''),
                        'inventory': snapshot_data.get('inventory', '')
                    })
            except Exception:
                continue
        
        # Sort by timestamp
        snapshots.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return snapshots
    
    def cleanup_old_snapshots(self, keep_count: int = 10) -> None:
        """Remove old snapshots, keeping only the most recent ones."""
        snapshots = self.list_snapshots()
        
        if len(snapshots) > keep_count:
            snapshots_to_delete = snapshots[keep_count:]
            
            for snapshot in snapshots_to_delete:
                snapshot_file = self.snapshot_dir / f"{snapshot['id']}.json"
                if snapshot_file.exists():
                    snapshot_file.unlink()
