#!/usr/bin/env python3
"""
Chaos Orchestrator

A whimsical Python script that orchestrates various chaos scenarios
based on environment variables.
"""

import os
import time
import random
import signal
import subprocess
import sys
import logging
import requests
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChaosOrchestrator:
    """Orchestrates various chaos scenarios"""
    
    def __init__(self):
        self.chaos_duration = self._parse_duration(
            os.environ.get('CHAOS_DURATION', '30m')
        )
        self.enable_network_chaos = os.environ.get(
            'ENABLE_NETWORK_CHAOS', 'true'
        ).lower() == 'true'
        self.network_latency_ms = int(os.environ.get(
            'NETWORK_LATENCY_MS', '200'
        ))
        self.enable_cpu_chaos = os.environ.get(
            'ENABLE_CPU_CHAOS', 'true'
        ).lower() == 'true'
        self.cpu_stress_duration = self._parse_duration(
            os.environ.get('CPU_STRESS_DURATION', '10m')
        )
        self.enable_random_failures = os.environ.get(
            'ENABLE_RANDOM_FAILURES', 'true'
        ).lower() == 'true'
        self.failure_rate = float(os.environ.get('FAILURE_RATE', '0.1'))
        self.whimsy_level = os.environ.get('WHIMSY_LEVEL', 'high')
        
        self.chaos_end_time = datetime.now() + timedelta(seconds=self.chaos_duration)
        self.running = True
        
        # Track running processes
        self.chaos_processes = []
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        logger.info(f"Chaos Orchestrator initialized")
        logger.info(f"Chaos duration: {self.chaos_duration} seconds")
        logger.info(f"Whimsy level: {self.whimsy_level}")
        logger.info(f"End time: {self.chaos_end_time}")
    
    def _parse_duration(self, duration_str):
        """Parse duration string like '30m', '1h', '2h30m' into seconds"""
        total_seconds = 0
        
        # Handle simple cases first
        if duration_str.endswith('m'):
            return int(duration_str[:-1]) * 60
        elif duration_str.endswith('h'):
            return int(duration_str[:-1]) * 3600
        elif duration_str.endswith('s'):
            return int(duration_str[:-1])
        
        # Handle complex cases like '2h30m'
        hours = 0
        minutes = 0
        seconds = 0
        
        if 'h' in duration_str:
            hours_str, duration_str = duration_str.split('h')
            hours = int(hours_str)
        
        if 'm' in duration_str:
            minutes_str, duration_str = duration_str.split('m')
            minutes = int(minutes_str)
        
        if 's' in duration_str and duration_str != '':
            seconds_str = duration_str[:-1]
            seconds = int(seconds_str)
        
        return hours * 3600 + minutes * 60 + seconds
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
        self._cleanup()
        sys.exit(0)
    
    def _cleanup(self):
        """Clean up running chaos processes"""
        logger.info("Cleaning up chaos processes...")
        for process in self.chaos_processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                logger.error(f"Error killing process: {e}")
        
        # Reset network changes
        self._reset_network_chaos()
    
    def _get_whimsical_message(self):
        """Get a whimsical message based on whimsy level"""
        messages = {
            'low': [
                "Maintaining system stability...",
                "Monitoring infrastructure health...",
                "All systems nominal..."
            ],
            'medium': [
                "Introducing mild chaos...",
                "Spicing up your infrastructure...",
                "Adding a dash of unpredictability..."
            ],
            'high': [
                "Unleashing the chaos gremlins!",
                "Mayhem mode activated!",
                "Chaos monkeys are at work!",
                "Embrace the chaos!",
                "Things are getting interesting..."
            ]
        }
        
        return random.choice(messages.get(self.whimsy_level, messages['high']))
    
    def _apply_network_chaos(self):
"""Apply network latency chaos using tc"""
        if not self.enable_network_chaos:
            return
        
        logger.info(f"Applying network chaos: {self.network_latency_ms}ms latency")
        try:
            # Add network delay
            cmd = [
                'tc', 'qdisc', 'add', 'dev', 'eth0', 'root',
                'netem', 'delay', f'{self.network_latency_ms}ms'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Failed to apply network chaos: {result.stderr}")
            else:
                logger.info("Network chaos applied successfully")
        except Exception as e:
            logger.error(f"Error applying network chaos: {e}")
    
    def _reset_network_chaos(self):
        """Reset network changes"""
        try:
            cmd = ['tc', 'qdisc', 'del', 'dev', 'eth0', 'root']
            subprocess.run(cmd, capture_output=True, text=True)
            logger.info("Network chaos reset")
        except Exception as e:
            logger.error(f"Error resetting network chaos: {e}")
    
    def _apply_cpu_chaos(self):
        """Apply CPU stress chaos"""
        if not self.enable_cpu_chaos:
            return
        
        logger.info(f"Applying CPU chaos for {self.cpu_stress_duration} seconds")
        try:
            # Start CPU stress in background
            cmd = ['stress-ng', '--cpu', '0', '--timeout', f'{self.cpu_stress_duration}s']
            process = subprocess.Popen(cmd)
            self.chaos_processes.append(process)
            logger.info("CPU chaos applied")
        except Exception as e:
            logger.error(f"Error applying CPU chaos: {e}")
    
    def _check_random_failures(self):
        """Check if we should induce a random failure"""
        if not self.enable_random_failures:
            return False
        
        if random.random() < self.failure_rate:
            logger.warning("Random failure induced!")
            return True
        return False
    
    def _health_check_server(self):
        """Start a simple health check server"""
        import threading
        from http.server import HTTPServer, BaseHTTPRequestHandler
        
        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        'status': 'healthy',
                        'timestamp': datetime.now().isoformat(),
                        'chaos_active': True
                    }
                    self.wfile.write(str(response).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
        
        def run_server():
            server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
            logger.info("Health check server started on port 8080")
            server.serve_forever()
        
        # Start health server in background
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
    
    def run(self):
        """Main chaos orchestration loop"""
        logger.info("Starting chaos orchestration")
        self._health_check_server()
        
        # Apply initial chaos
        self._apply_network_chaos()
        self._apply_cpu_chaos()
        
        # Main loop
        while self.running and datetime.now() < self.chaos_end_time:
            # Log whimsical message
            whimsical_msg = self._get_whimsical_message()
            logger.info(whimsical_msg)
            
            # Check for random failures
            if self._check_random_failures():
                # Simulate a failure by sleeping briefly
                time.sleep(random.uniform(1, 5))
            
            # Small delay before next iteration
            time.sleep(random.uniform(10, 30))
        
        logger.info("Chaos duration complete, cleaning up...")
        self._cleanup()
        logger.info("Chaos orchestration complete!")


if __name__ == '__main__':
    orchestrator = ChaosOrchestrator()
    orchestrator.run()
