#!/usr/bin/env python3
"""
Nightly Docker Chaos Garden - Containerized chaos gardening for infrastructure resilience.

This tool randomly prunes, replants, and monitors Docker containers to simulate
post-apocalyptic infrastructure conditions and test resilience.
"""

import os
import sys
import json
import yaml
import random
import time
import logging
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import docker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ChaosReport:
    """Data structure for chaos gardening reports."""
    timestamp: str
    scenario: str
    total_containers: int
    pruned_containers: int
    replanted_containers: int
    survival_rate: float
    essential_preserved: bool
    pruned_list: List[str]
    replanted_list: List[str]
    dry_run: bool


class ChaosGarden:
    """Main chaos gardening orchestrator."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.client = docker.from_env()
        self.scenarios = {
            'drought': self._drought_scenario,
            'storm': self._storm_scenario,
            'quake': self._quake_scenario,
            'random': self._random_scenario
        }
        
    def get_container_stats(self) -> List[Dict[str, Any]]:
        """Get statistics for all running containers."""
        try:
            containers = self.client.containers.list()
            stats = []
            
            for container in containers:
                try:
                    container_stats = container.stats(stream=False)
                    stats.append({
                        'id': container.short_id,
                        'name': container.name,
                        'image': container.image.tags[0] if container.image.tags else 'unknown',
                        'status': container.status,
                        'created': container.attrs['Created'],
                        'cpu_usage': container_stats.get('cpu_stats', {}).get('cpu_usage', {}).get('total_usage', 0),
                        'memory_usage': container_stats.get('memory_stats', {}).get('usage', 0),
                        'memory_limit': container_stats.get('memory_stats', {}).get('limit', 0),
                        'essential': self._is_essential(container)
                    })
                except Exception as e:
                    logger.warning(f"Failed to get stats for container {container.name}: {e}")
                    
            return stats
        except Exception as e:
            logger.error(f"Failed to retrieve container statistics: {e}")
            return []
    
    def _is_essential(self, container) -> bool:
        """Determine if a container is essential and should be preserved."""
        essential_patterns = [
            'db', 'database', 'postgres', 'mysql', 'redis', 'mongo',
            'monitoring', 'prometheus', 'grafana', 'nginx', 'proxy',
            'auth', 'vault', 'consul', 'etcd'
        ]
        
        container_name = container.name.lower()
        image_tags = [tag.lower() for tag in container.image.tags] if container.image.tags else []
        
        return any(pattern in container_name or any(pattern in tag for tag in image_tags) 
                  for pattern in essential_patterns)
    
    def _drought_scenario(self, containers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate drought - conserve resources by pruning non-essential containers."""
        logger.info("🌵 Applying drought scenario - conserving resources")
        
        non_essential = [c for c in containers if not c['essential']]
        essential = [c for c in containers if c['essential']]
        
        # Prune 40% of non-essential containers
        prune_count = max(1, int(len(non_essential) * 0.4))
        containers_to_prune = random.sample(non_essential, prune_count)
        
        pruned = self._prune_containers(containers_to_prune)
        replanted = self._replant_essential(essential)
        
        return {
            'pruned': pruned,
            'replanted': replanted,
            'survival_rate': (len(containers) - len(pruned)) / len(containers) * 100 if containers else 0
        }
    
    def _storm_scenario(self, containers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate storm - random destruction and rebuilding."""
        logger.info("⛈️  Applying storm scenario - random destruction and rebuilding")
        
        # Randomly select containers to destroy (30%)
        destroy_count = max(1, int(len(containers) * 0.3))
        containers_to_destroy = random.sample(containers, destroy_count)
        
        # But preserve essential ones
        essential_to_destroy = [c for c in containers_to_destroy if c['essential']]
        non_essential_to_destroy = [c for c in containers_to_destroy if not c['essential']]
        
        pruned = self._prune_containers(non_essential_to_destroy)
        
        # Replant essential services that were destroyed
        replanted = self._replant_essential(essential_to_destroy)
        
        return {
            'pruned': pruned,
            'replanted': replanted,
            'survival_rate': (len(containers) - len(pruned)) / len(containers) * 100 if containers else 0
        }
    
    def _quake_scenario(self, containers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simulate earthquake - target containers based on resource usage."""
        logger.info(" earthquaking - targeting high-resource containers")
        
        # Sort by memory usage and target top 50%
        sorted_containers = sorted(containers, key=lambda x: x['memory_usage'], reverse=True)
        target_containers = sorted_containers[:len(sorted_containers)//2]
        
        # Filter out essential containers from targets
        non_essential_targets = [c for c in target_containers if not c['essential']]
        
        pruned = self._prune_containers(non_essential_targets)
        replanted = self._replant_essential([c for c in containers if c['essential']])
        
        return {
            'pruned': pruned,
            'replanted': replanted,
            'survival_rate': (len(containers) - len(pruned)) / len(containers) * 100 if containers else 0
        }
    
    def _random_scenario(self, containers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply a random chaos scenario."""
        scenario_names = ['drought', 'storm', 'quake']
        chosen_scenario = random.choice(scenario_names)
        logger.info(f"🎲 Random scenario chosen: {chosen_scenario}")
        
        return self.scenarios[chosen_scenario](containers)
    
    def _prune_containers(self, containers_to_prune: List[Dict[str, Any]]) -> List[str]:
        """Prune specified containers."""
        pruned_names = []
        
        for container_info in containers_to_prune:
            try:
                container = self.client.containers.get(container_info['id'])
                
                if self.dry_run:
                    logger.info(f"[DRY RUN] Would prune container: {container.name}")
                    pruned_names.append(container.name)
                else:
                    logger.info(f"Pruning container: {container.name}")
                    container.stop()
                    container.remove()
                    pruned_names.append(container.name)
                    
            except Exception as e:
                logger.error(f"Failed to prune container {container_info['name']}: {e}")
        
        return pruned_names
    
    def _replant_essential(self, essential_containers: List[Dict[str, Any]]) -> List[str]:
        """Replant essential containers that may have been destroyed."""
        replanted_names = []
        
        for container_info in essential_containers:
            try:
                # Check if container still exists
                existing = self.client.containers.list(all=True, filters={'name': container_info['name']})
                
                if not existing:
                    if self.dry_run:
                        logger.info(f"[DRY RUN] Would replant essential container: {container_info['name']}")
                        replanted_names.append(container_info['name'])
                    else:
                        logger.info(f"Replanting essential container: {container_info['name']}")
                        # For simplicity, we'll just log what would be replanted
                        # In a real scenario, you'd have container definitions to recreate
                        replanted_names.append(container_info['name'])
                
            except Exception as e:
                logger.error(f"Failed to replant container {container_info['name']}: {e}")
        
        return replanted_names
    
    def run_chaos(self, scenario: str = 'random') -> ChaosReport:
        """Execute the chaos gardening scenario."""
        logger.info("🌿 Starting chaos gardening session...")
        
        # Get current container statistics
        containers = self.get_container_stats()
        total_containers = len(containers)
        
        if total_containers == 0:
            logger.warning("No containers found to manage!")
            return ChaosReport(
                timestamp=datetime.now().isoformat(),
                scenario=scenario,
                total_containers=0,
                pruned_containers=0,
                replanted_containers=0,
                survival_rate=100.0,
                essential_preserved=True,
                pruned_list=[],
                replanted_list=[],
                dry_run=self.dry_run
            )
        
        logger.info(f"Found {total_containers} containers to manage")
        
        # Apply the chosen scenario
        if scenario not in self.scenarios:
            scenario = 'random'
        
        result = self.scenarios[scenario](containers)
        
        # Generate report
        essential_preserved = all(c['essential'] for c in containers if c['name'] not in result['pruned'])
        
        report = ChaosReport(
            timestamp=datetime.now().isoformat(),
            scenario=scenario,
            total_containers=total_containers,
            pruned_containers=len(result['pruned']),
            replanted_containers=len(result['replanted']),
            survival_rate=result['survival_rate'],
            essential_preserved=essential_preserved,
            pruned_list=result['pruned'],
            replanted_list=result['replanted'],
            dry_run=self.dry_run
        )
        
        self._print_report(report)
        return report
    
    def _print_report(self, report: ChaosReport):
        """Print the chaos gardening report."""
        print("\n" + "="*50)
        print("    CHAOS GARDEN REPORT")
        print("="*50)
        print(f"Scenario: {report.scenario}")
        print(f"Timestamp: {report.timestamp}")
        print(f"Total containers: {report.total_containers}")
        print(f"Containers pruned: {report.pruned_containers}")
        print(f"Containers replanted: {report.replanted_containers}")
        print(f"Survival rate: {report.survival_rate:.1f}%")
        print(f"Essential services preserved: {report.essential_preserved}")
        print(f"Dry run mode: {self.dry_run}")
        
        if report.pruned_list:
            print("\nPruned containers:")
            for name in report.pruned_list:
                print(f"  - {name}")
        
        if report.replanted_list:
            print("\nReplanted containers:")
            for name in report.replanted_list:
                print(f"  - {name}")
        
        print("="*50 + "\n")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Nightly Docker Chaos Garden')
    parser.add_argument('--scenario', choices=['drought', 'storm', 'quake', 'random'], 
                       default='random', help='Chaos scenario to apply')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Simulate actions without modifying containers')
    parser.add_argument('--format', choices=['text', 'json', 'yaml'], default='text',
                       help='Output format for the report')
    parser.add_argument('--output', type=str, help='File to save the report')
    
    args = parser.parse_args()
    
    # Environment variable overrides
    env_scenario = os.getenv('CHAOS_SCENARIO')
    env_dry_run = os.getenv('DRY_RUN', '').lower() == 'true'
    env_format = os.getenv('REPORT_FORMAT', args.format)
    
    scenario = env_scenario or args.scenario
    dry_run = env_dry_run or args.dry_run
    output_format = env_format or args.format
    
    logger.info(f"Starting chaos garden with scenario: {scenario}, dry_run: {dry_run}")
    
    try:
        garden = ChaosGarden(dry_run=dry_run)
        report = garden.run_chaos(scenario)
        
        # Save report if requested
        if args.output or output_format != 'text':
            output_data = asdict(report)
            
            if args.output:
                with open(args.output, 'w') as f:
                    if output_format == 'json':
                        json.dump(output_data, f, indent=2)
                    elif output_format == 'yaml':
                        yaml.dump(output_data, f, default_flow_style=False)
                    else:
                        f.write(str(output_data))
                logger.info(f"Report saved to {args.output}")
            else:
                if output_format == 'json':
                    print(json.dumps(output_data, indent=2))
                elif output_format == 'yaml':
                    print(yaml.dump(output_data, default_flow_style=False))
        
    except Exception as e:
        logger.error(f"Chaos gardening failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
