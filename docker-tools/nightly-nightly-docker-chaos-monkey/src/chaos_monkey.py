#!/usr/bin/env python3
"""
Nightly Docker Chaos Monkey

A whimsical-yet-useful containerized chaos engineering tool that randomly
injects failures into Docker environments for resilience testing.
"""

import os
import sys
import time
import random
import json
import logging
import argparse
import signal
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

import docker
import psutil
from flask import Flask, jsonify, request
from flask_cors import CORS
from pythonjsonlogger import jsonlogger


@dataclass
class ChaosConfig:
    """Configuration for chaos monkey behavior."""
    duration: int = 300  # 0 = infinite
    intensity: str = "medium"
    interval: int = 60
    target_label: str = "chaos.monkey=true"
    network_delay: int = 100
    memory_pressure: int = 50
    cpu_stress: int = 80
    dry_run: bool = False
    log_level: str = "INFO"


@dataclass
class ChaosEvent:
    """Represents a chaos event that occurred."""
    timestamp: str
    event_type: str
    target: str
    intensity: str
    success: bool
    details: Dict[str, Any]


class ChaosMonkey:
    """Main chaos monkey implementation."""
    
    def __init__(self, config: ChaosConfig):
        self.config = config
        self.docker_client = docker.from_env()
        self.logger = self._setup_logger()
        self.running = False
        self.start_time = None
        self.events: List[ChaosEvent] = []
        self.event_lock = threading.Lock()
        
        # Chaos event handlers
        self.event_handlers = {
            "container_kill": self._kill_container,
            "cpu_spike": self._cpu_spike,
            "memory_pressure": self._memory_pressure,
            "network_latency": self._network_latency,
            "disk_io": self._disk_io_pressure,
            "random_restart": self._random_restart,
        }
        
        # Intensity multipliers
        self.intensity_multipliers = {
            "low": 0.3,
            "medium": 0.6,
            "high": 1.0
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup structured JSON logging."""
        logger = logging.getLogger("chaos_monkey")
        logger.setLevel(getattr(logging, self.config.log_level.upper()))
        
        # Create JSON formatter
        log_handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        
        return logger
    
    def _get_target_containers(self) -> List[docker.models.containers.Container]:
        """Get containers that have the chaos monkey label."""
        try:
            containers = self.docker_client.containers.list()
            target_containers = []
            
            for container in containers:
                if container.labels.get(self.config.target_label) == "true":
                    # Skip the chaos monkey itself
                    if container.name != "chaos-monkey":
                        target_containers.append(container)
            
            return target_containers
        except Exception as e:
            self.logger.error(f"Failed to get target containers: {e}")
            return []
    
    def _record_event(self, event: ChaosEvent):
        """Record a chaos event."""
        with self.event_lock:
            self.events.append(event)
            # Keep only last 100 events
            if len(self.events) > 100:
                self.events.pop(0)
    
    def _should_stop(self) -> bool:
        """Check if chaos monkey should stop."""
        if not self.running:
            return True
        
        if self.config.duration > 0:
            elapsed = time.time() - self.start_time
            if elapsed >= self.config.duration:
                return True
        
        return False
    
    def _get_intensity_multiplier(self) -> float:
        """Get intensity multiplier based on configuration."""
        return self.intensity_multipliers.get(self.config.intensity, 0.6)
    
    def _kill_container(self, container: docker.models.containers.Container) -> bool:
        """Kill a container."""
        try:
            if self.config.dry_run:
                self.logger.info(f"[DRY RUN] Would kill container: {container.name}")
                return True
            
            container.kill()
            self.logger.info(f"Killed container: {container.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to kill container {container.name}: {e}")
            return False
    
    def _cpu_spike(self, container: docker.models.containers.Container) -> bool:
        """Create CPU spike in a container."""
        try:
            multiplier = self._get_intensity_multiplier()
            cpu_limit = int(100 * multiplier)
            
            if self.config.dry_run:
                self.logger.info(f"[DRY RUN] Would spike CPU for container: {container.name} (limit: {cpu_limit}%)")
                return True
            
            # Update container with CPU limit
            container.update(cpu_quota=int(cpu_limit * 1000))
            self.logger.info(f"Applied CPU spike to container: {container.name} (limit: {cpu_limit}%)")
            
            # Reset after a short delay
            def reset_cpu():
                time.sleep(10)
                try:
                    container.update(cpu_quota=-1)
                    self.logger.info(f"Reset CPU limit for container: {container.name}")
                except Exception as e:
                    self.logger.error(f"Failed to reset CPU limit for {container.name}: {e}")
            
            threading.Thread(target=reset_cpu, daemon=True).start()
            return True
        except Exception as e:
            self.logger.error(f"Failed to apply CPU spike to {container.name}: {e}")
            return False
    
    def _memory_pressure(self, container: docker.models.containers.Container) -> bool:
        """Create memory pressure in a container."""
        try:
            multiplier = self._get_intensity_multiplier()
            memory_limit = int(512 * 1024 * 1024 * multiplier)  # 512MB base
            
            if self.config.dry_run:
                self.logger.info(f"[DRY RUN] Would apply memory pressure to container: {container.name} (limit: {memory_limit} bytes)")
                return True
            
            container.update(mem_limit=memory_limit)
            self.logger.info(f"Applied memory pressure to container: {container.name} (limit: {memory_limit} bytes)")
            
            # Reset after a short delay
            def reset_memory():
                time.sleep(15)
                try:
                    container.update(mem_limit=-1)
                    self.logger.info(f"Reset memory limit for container: {container.name}")
                except Exception as e:
                    self.logger.error(f"Failed to reset memory limit for {container.name}: {e}")
            
            threading.Thread(target=reset_memory, daemon=True).start()
            return True
        except Exception as e:
            self.logger.error(f"Failed to apply memory pressure to {container.name}: {e}")
            return False
    
    def _network_latency(self, container: docker.models.containers.Container) -> bool:
        """Add network latency to a container."""
        try:
            multiplier = self._get_intensity_multiplier()
            delay = int(self.config.network_delay * multiplier)
            
            if self.config.dry_run:
                self.logger.info(f"[DRY RUN] Would add network latency to container: {container.name} (delay: {delay}ms)")
                return True
            
            # Get container PID
            container_info = container.attrs
            pid = container_info['State']['Pid']
            
            # Add network delay using tc (traffic control)
            cmd = f"tc qdisc add dev eth0 root netem delay {delay}ms"
            exec_result = container.exec_run(cmd, privileged=True)
            
            if exec_result.exit_code == 0:
                self.logger.info(f"Added network latency to container: {container.name} (delay: {delay}ms)")
                
                # Remove delay after a short delay
                def remove_latency():
                    time.sleep(10)
                    try:
                        container.exec_run("tc qdisc del dev eth0 root", privileged=True)
                        self.logger.info(f"Removed network latency from container: {container.name}")
                    except Exception as e:
                        self.logger.error(f"Failed to remove network latency from {container.name}: {e}")
                
                threading.Thread(target=remove_latency, daemon=True).start()
                return True
            else:
                self.logger.error(f"Failed to add network latency to {container.name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to add network latency to {container.name}: {e}")
            return False
    
    def _disk_io_pressure(self, container: docker.models.containers.Container) -> bool:
        """Create disk I/O pressure in a container."""
        try:
            if self.config.dry_run:
                self.logger.info(f"[DRY RUN] Would create disk I/O pressure in container: {container.name}")
                return True
            
            # Run a disk I/O stress test
            cmd = "dd if=/dev/zero of=/tmp/testfile bs=1M count=100 oflag=direct"
            exec_result = container.exec_run(cmd)
            
            if exec_result.exit_code == 0:
                self.logger.info(f"Created disk I/O pressure in container: {container.name}")
                return True
            else:
                self.logger.error(f"Failed to create disk I/O pressure in {container.name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to create disk I/O pressure in {container.name}: {e}")
            return False
    
    def _random_restart(self, container: docker.models.containers.Container) -> bool:
        """Randomly restart a container."""
        try:
            if self.config.dry_run:
                self.logger.info(f"[DRY RUN] Would restart container: {container.name}")
                return True
            
            container.restart()
            self.logger.info(f"Restarted container: {container.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to restart container {container.name}: {e}")
            return False
    
    def _execute_chaos_event(self):
        """Execute a random chaos event."""
        target_containers = self._get_target_containers()
        
        if not target_containers:
            self.logger.info("No target containers found. Waiting for labeled containers...")
            return
        
        # Select random container
        target_container = random.choice(target_containers)
        
        # Select random event type
        event_type = random.choice(list(self.event_handlers.keys()))
        
        self.logger.info(f"Executing chaos event: {event_type} on container: {target_container.name}")
        
        # Execute the event
        start_time = time.time()
        success = self.event_handlers[event_type](target_container)
        duration = time.time() - start_time
        
        # Record the event
        event = ChaosEvent(
            timestamp=datetime.utcnow().isoformat(),
            event_type=event_type,
            target=target_container.name,
            intensity=self.config.intensity,
            success=success,
            details={
                "duration": duration,
                "container_id": target_container.short_id,
                "dry_run": self.config.dry_run
            }
        )
        
        self._record_event(event)
        
        # Log result
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"Chaos event {status}: {event_type} on {target_container.name} (duration: {duration:.2f}s)")
    
    def run(self):
        """Main chaos monkey execution loop."""
        self.logger.info("Starting Chaos Monkey")
        self.logger.info(f"Configuration: {asdict(self.config)}")
        
        self.running = True
        self.start_time = time.time()
        
        try:
            while not self._should_stop():
                self._execute_chaos_event()
                
                # Wait for next interval
                time.sleep(self.config.interval)
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal, shutting down...")
        finally:
            self.running = False
            self.logger.info("Chaos Monkey stopped")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get chaos monkey statistics."""
        with self.event_lock:
            total_events = len(self.events)
            successful_events = sum(1 for event in self.events if event.success)
            failed_events = total_events - successful_events
            
            event_types = {}
            for event in self.events:
                event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
            
            return {
                "total_events": total_events,
                "successful_events": successful_events,
                "failed_events": failed_events,
                "success_rate": successful_events / total_events if total_events > 0 else 0,
                "event_types": event_types,
                "running": self.running,
                "start_time": datetime.fromtimestamp(self.start_time).isoformat() if self.start_time else None,
                "uptime": time.time() - self.start_time if self.start_time else 0
            }


class ChaosMonkeyAPI:
    """Flask API for chaos monkey monitoring and control."""
    
    def __init__(self, chaos_monkey: ChaosMonkey):
        self.chaos_monkey = chaos_monkey
        self.app = Flask(__name__)
        CORS(self.app)
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes."""
        @self.app.route('/health')
        def health():
            return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})
        
        @self.app.route('/stats')
        def stats():
            return jsonify(self.chaos_monkey.get_stats())
        
        @self.app.route('/events')
        def events():
            with self.chaos_monkey.event_lock:
                return jsonify([asdict(event) for event in self.chaos_monkey.events])
        
        @self.app.route('/config')
        def config():
            return jsonify(asdict(self.chaos_monkey.config))
        
        @self.app.route('/stop', methods=['POST'])
        def stop():
            self.chaos_monkey.running = False
            return jsonify({"message": "Chaos Monkey stopping..."})
        
        @self.app.route('/chaos', methods=['POST'])
        def manual_chaos():
            """Trigger a manual chaos event."""
            try:
                self.chaos_monkey._execute_chaos_event()
                return jsonify({"message": "Manual chaos event triggered"})
            except Exception as e:
                return jsonify({"error": str(e)}), 500
    
    def run(self, host='0.0.0.0', port=8080, debug=False):
        """Run the Flask API."""
        self.app.run(host=host, port=port, debug=debug)


def parse_args() -> ChaosConfig:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Nightly Docker Chaos Monkey')
    parser.add_argument('--duration', type=int, default=300,
                       help='Duration in seconds to run chaos (0 = infinite)')
    parser.add_argument('--intensity', choices=['low', 'medium', 'high'], default='medium',
                       help='Chaos intensity level')
    parser.add_argument('--interval', type=int, default=60,
                       help='Interval in seconds between chaos events')
    parser.add_argument('--target-label', default='chaos.monkey=true',
                       help='Docker label to identify target containers')
    parser.add_argument('--network-delay', type=int, default=100,
                       help='Network delay in milliseconds')
    parser.add_argument('--memory-pressure', type=int, default=50,
                       help='Memory pressure percentage (0-100)')
    parser.add_argument('--cpu-stress', type=int, default=80,
                       help='CPU stress percentage (0-100)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would happen without executing')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO',
                       help='Log level')
    
    args = parser.parse_args()
    
    # Override with environment variables if present
    env_config = {
        'duration': int(os.getenv('CHAOS_DURATION', args.duration)),
        'intensity': os.getenv('CHAOS_INTENSITY', args.intensity),
        'interval': int(os.getenv('CHAOS_INTERVAL', args.interval)),
        'target_label': os.getenv('CHAOS_TARGET_LABEL', args.target_label),
        'network_delay': int(os.getenv('CHAOS_NETWORK_DELAY', args.network_delay)),
        'memory_pressure': int(os.getenv('CHAOS_MEMORY_PRESSURE', args.memory_pressure)),
        'cpu_stress': int(os.getenv('CHAOS_CPU_STRESS', args.cpu_stress)),
        'dry_run': os.getenv('CHAOS_DRY_RUN', str(args.dry_run)).lower() == 'true',
        'log_level': os.getenv('CHAOS_LOG_LEVEL', args.log_level),
    }
    
    return ChaosConfig(**env_config)


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print("\nReceived shutdown signal. Exiting...")
    sys.exit(0)


def main():
    """Main entry point."""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse configuration
    config = parse_args()
    
    # Create chaos monkey
    chaos_monkey = ChaosMonkey(config)
    
    # Start API server in background thread
    api = ChaosMonkeyAPI(chaos_monkey)
    api_thread = threading.Thread(target=api.run, daemon=True)
    api_thread.start()
    
    # Run chaos monkey
    chaos_monkey.run()


if __name__ == '__main__':
    main()
