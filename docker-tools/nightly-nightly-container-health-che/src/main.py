import os
import sys
import time
import yaml
import json
import logging
import argparse
import subprocess
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import signal

# ANSI color codes for terminal output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

# Health status enumeration
class HealthStatus(Enum):
    HEALTHY = "🟢"
    WARNING = "🟡"
    CRITICAL = "🔴"
    UNKNOWN = "⚪"

@dataclass
class ContainerMetrics:
    name: str
    cpu_percent: float
    memory_usage: float  # MB
    memory_limit: float  # MB
    memory_percent: float
    disk_read: float     # MB
    disk_write: float    # MB
    network_rx: float    # MB
    network_tx: float    # MB
    status: HealthStatus
    timestamp: datetime

@dataclass
class AlertConfig:
    cpu_threshold: float = 80.0
    memory_threshold: float = 85.0
    disk_threshold: float = 90.0
    network_threshold: float = 1000.0

@dataclass
class MonitoringConfig:
    interval: int = 5
    containers: List[str] = None

@dataclass
class NotificationConfig:
    console: bool = True
    file: Optional[str] = None
    email: Optional[str] = None

@dataclass
class AppConfig:
    monitoring: MonitoringConfig
    alerts: AlertConfig
    notifications: NotificationConfig


class DockerHealthChecker:
    def __init__(self, config: AppConfig):
        self.config = config
        self.running = False
        self.metrics_history: Dict[str, List[ContainerMetrics]] = {}
        self.alert_history: List[Dict[str, Any]] = []
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_container_list(self) -> List[str]:
        """Get list of containers to monitor"""
        if self.config.monitoring.containers:
            return self.config.monitoring.containers
        
        try:
            result = subprocess.run(
                ['docker', 'ps', '--format', '{{.Names}}'],
                capture_output=True,
                text=True,
                check=True
            )
            containers = result.stdout.strip().split('\n')
            return [c for c in containers if c]  # Filter out empty strings
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to get container list: {e}")
            return []
    
    def get_container_stats(self, container_name: str) -> Optional[ContainerMetrics]:
        """Get real-time stats for a container"""
        try:
            result = subprocess.run(
                ['docker', 'stats', '--no-stream', '--format', 
                 'json', container_name],
                capture_output=True,
                text=True,
                check=True
            )
            
            stats = json.loads(result.stdout.strip())
            
            # Parse memory usage (format: "123.45MiB")
            memory_usage_str = stats['MemUsage'].split('/')[0].strip()
            memory_limit_str = stats['MemUsage'].split('/')[-1].strip()
            
            memory_usage = self.parse_memory_value(memory_usage_str)
            memory_limit = self.parse_memory_value(memory_limit_str)
            memory_percent = float(stats['MemPerc'].rstrip('%'))
            
            # Parse network I/O (format: "123.45MB")
            network_rx = self.parse_memory_value(stats['NetIO'].split(' / ')[0].strip())
            network_tx = self.parse_memory_value(stats['NetIO'].split(' / ')[1].strip())
            
            # Parse block I/O (format: "123.45MB")
            disk_read = self.parse_memory_value(stats['BlockIO'].split(' / ')[0].strip())
            disk_write = self.parse_memory_value(stats['BlockIO'].split(' / ')[1].strip())
            
            cpu_percent = float(stats['CPUPerc'].rstrip('%'))
            
            status = self.calculate_health_status(
                cpu_percent, memory_percent, disk_read, network_rx
            )
            
            metrics = ContainerMetrics(
                name=container_name,
                cpu_percent=cpu_percent,
                memory_usage=memory_usage,
                memory_limit=memory_limit,
                memory_percent=memory_percent,
                disk_read=disk_read,
                disk_write=disk_write,
                network_rx=network_rx,
                network_tx=network_tx,
                status=status,
                timestamp=datetime.now()
            )
            
            return metrics
            
        except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as e:
            self.logger.warning(f"Failed to get stats for {container_name}: {e}")
            return None
    
    def parse_memory_value(self, value_str: str) -> float:
        """Parse memory values like '123.45MiB' to float in MB"""
        try:
            if 'GiB' in value_str:
                return float(value_str.replace('GiB', '')) * 1024
            elif 'MiB' in value_str:
                return float(value_str.replace('MiB', ''))
            elif 'KiB' in value_str:
                return float(value_str.replace('KiB', '')) / 1024
            elif 'B' in value_str:
                return float(value_str.replace('B', '')) / (1024 * 1024)
            else:
                return float(value_str)
        except ValueError:
            return 0.0
    
    def calculate_health_status(self, cpu: float, memory: float, 
                              disk: float, network: float) -> HealthStatus:
        """Calculate health status based on thresholds"""
        if (cpu > self.config.alerts.cpu_threshold or
            memory > self.config.alerts.memory_threshold or
            disk > self.config.alerts.disk_threshold or
            network > self.config.alerts.network_threshold):
            return HealthStatus.CRITICAL
        elif (cpu > self.config.alerts.cpu_threshold * 0.8 or
              memory > self.config.alerts.memory_threshold * 0.8):
            return HealthStatus.WARNING
        else:
            return HealthStatus.HEALTHY
    
    def check_alerts(self, metrics: ContainerMetrics):
        """Check if metrics exceed thresholds and trigger alerts"""
        alerts = []
        
        if metrics.cpu_percent > self.config.alerts.cpu_threshold:
            alerts.append(f"High CPU usage: {metrics.cpu_percent:.1f}%")
        
        if metrics.memory_percent > self.config.alerts.memory_threshold:
            alerts.append(f"High memory usage: {metrics.memory_percent:.1f}%")
        
        if metrics.disk_read > self.config.alerts.disk_threshold:
            alerts.append(f"High disk read: {metrics.disk_read:.1f}MB")
        
        if metrics.network_rx > self.config.alerts.network_threshold:
            alerts.append(f"High network RX: {metrics.network_rx:.1f}MB")
        
        if alerts:
            alert_data = {
                'timestamp': metrics.timestamp.isoformat(),
                'container': metrics.name,
                'status': metrics.status.value,
                'alerts': alerts,
                'metrics': asdict(metrics)
            }
            self.alert_history.append(alert_data)
            self.send_notifications(alert_data)
    
    def send_notifications(self, alert_data: Dict[str, Any]):
        """Send alert notifications"""
        if self.config.notifications.console:
            self.display_console_alert(alert_data)
        
        if self.config.notifications.file:
            self.write_alert_to_file(alert_data)
    
    def display_console_alert(self, alert_data: Dict[str, Any]):
        """Display alert in console with color coding"""
        container = alert_data['container']
        status = alert_data['status']
        alerts = alert_data['alerts']
        
        color = Colors.RED if status == HealthStatus.CRITICAL.value else Colors.YELLOW
        
        print(f"\n{color}{status} ALERT: Container '{container}'{Colors.RESET}")
        print(f"{color}{'=' * 50}{Colors.RESET}")
        for alert in alerts:
            print(f"{color}⚠️  {alert}{Colors.RESET}")
        print(f"{color}{'=' * 50}{Colors.RESET}\n")
    
    def write_alert_to_file(self, alert_data: Dict[str, Any]):
        """Write alert to log file"""
        try:
            with open(self.config.notifications.file, 'a') as f:
                f.write(json.dumps(alert_data) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write alert to file: {e}")
    
    def display_dashboard(self, metrics_list: List[ContainerMetrics]):
        """Display real-time dashboard"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════════════════════╗")
        print("║                           Container Health Dashboard                         ║")
        print("╠══════════════════════════════════════════════════════════════════════════════╣")
        print(f"{Colors.RESET}")
        
        for metrics in metrics_list:
            if metrics is None:
                continue
                
            status_color = {
                HealthStatus.HEALTHY: Colors.GREEN,
                HealthStatus.WARNING: Colors.YELLOW,
                HealthStatus.CRITICAL: Colors.RED,
                HealthStatus.UNKNOWN: Colors.WHITE
            }.get(metrics.status, Colors.WHITE)
            
            print(f"{status_color}{metrics.status.value}{Colors.RESET} ", end="")
            print(f"Container: {metrics.name:<15} ", end="")
            print(f"Status: {status_color}{metrics.status.name:<8}{Colors.RESET} ", end="")
            print(f"CPU: {metrics.cpu_percent:>5.1f}% ", end="")
            print(f"Memory: {metrics.memory_usage:>6.1f}MB ", end="")
            print(f"({metrics.memory_percent:>4.1f}%)")
        
        print(f"{Colors.CYAN}")
        print("╚══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{Colors.RESET}")
        print(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Press Ctrl+C to exit")
    
    def monitor_containers(self):
        """Main monitoring loop"""
        self.running = True
        
        def signal_handler(signum, frame):
            print("\nShutting down gracefully...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            while self.running:
                containers = self.get_container_list()
                
                if not containers:
                    print("No containers found to monitor.")
                    time.sleep(self.config.monitoring.interval)
                    continue
                
                metrics_list = []
                
                for container in containers:
                    metrics = self.get_container_stats(container)
                    if metrics:
                        self.check_alerts(metrics)
                        metrics_list.append(metrics)
                        
                        # Store in history
                        if container not in self.metrics_history:
                            self.metrics_history[container] = []
                        self.metrics_history[container].append(metrics)
                        
                        # Keep only last 100 entries per container
                        if len(self.metrics_history[container]) > 100:
                            self.metrics_history[container].pop(0)
                    else:
                        # Container not found, add unknown status
                        unknown_metrics = ContainerMetrics(
                            name=container,
                            cpu_percent=0.0,
                            memory_usage=0.0,
                            memory_limit=0.0,
                            memory_percent=0.0,
                            disk_read=0.0,
                            disk_write=0.0,
                            network_rx=0.0,
                            network_tx=0.0,
                            status=HealthStatus.UNKNOWN,
                            timestamp=datetime.now()
                        )
                        metrics_list.append(unknown_metrics)
                
                self.display_dashboard(metrics_list)
                time.sleep(self.config.monitoring.interval)
                
        except KeyboardInterrupt:
            self.running = False
        
        print("\nMonitoring stopped.")
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {},
            'containers': {},
            'alerts': self.alert_history
        }
        
        for container_name, history in self.metrics_history.items():
            if not history:
                continue
                
            latest = history[-1]
            
            report['containers'][container_name] = {
                'current_status': latest.status.name,
                'latest_metrics': asdict(latest),
                'avg_cpu': sum(m.cpu_percent for m in history) / len(history),
                'max_cpu': max(m.cpu_percent for m in history),
                'avg_memory': sum(m.memory_usage for m in history) / len(history),
                'max_memory': max(m.memory_usage for m in history),
                'recommendations': self.generate_recommendations(history)
            }
        
        # Generate summary
        total_containers = len(self.metrics_history)
        healthy_containers = sum(1 for h in self.metrics_history.values() 
                               if h and h[-1].status == HealthStatus.HEALTHY)
        warning_containers = sum(1 for h in self.metrics_history.values() 
                               if h and h[-1].status == HealthStatus.WARNING)
        critical_containers = sum(1 for h in self.metrics_history.values() 
                                if h and h[-1].status == HealthStatus.CRITICAL)
        
        report['summary'] = {
            'total_containers': total_containers,
            'healthy_containers': healthy_containers,
            'warning_containers': warning_containers,
            'critical_containers': critical_containers,
            'overall_health': 'HEALTHY' if critical_containers == 0 else 'CRITICAL'
        }
        
        return report
    
    def generate_recommendations(self, history: List[ContainerMetrics]) -> List[str]:
        """Generate recommendations based on historical data"""
        recommendations = []
        
        if not history:
            return recommendations
        
        avg_cpu = sum(m.cpu_percent for m in history) / len(history)
        avg_memory = sum(m.memory_usage for m in history) / len(history)
        max_cpu = max(m.cpu_percent for m in history)
        max_memory = max(m.memory_usage for m in history)
        
        if max_cpu > 90:
            recommendations.append("Consider scaling up CPU resources or optimizing application code")
        
        if max_memory > history[0].memory_limit * 0.9:
            recommendations.append("Consider increasing memory allocation for this container")
        
        if len([m for m in history if m.status == HealthStatus.CRITICAL]) > len(history) * 0.1:
            recommendations.append("Container frequently hits critical thresholds - investigate root cause")
        
        if not recommendations:
            recommendations.append("Container performance looks good!")
        
        return recommendations

def load_config(config_path: str) -> AppConfig:
    """Load configuration from YAML file"""
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

def main():
    parser = argparse.ArgumentParser(description='Docker Container Health Checker')
    parser.add_argument('--config', '-c', default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--containers', '-C', nargs='+',
                       help='Specific containers to monitor (overrides config)')
    parser.add_argument('--cpu-threshold', type=float,
                       help='CPU alert threshold (overrides config)')
    parser.add_argument('--memory-threshold', type=float,
                       help='Memory alert threshold (overrides config)')
    parser.add_argument('--report', '-r', action='store_true',
                       help='Generate health report and exit')
    
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    
    # Override with command line args if provided
    if args.containers:
        config.monitoring.containers = args.containers
    if args.cpu_threshold:
        config.alerts.cpu_threshold = args.cpu_threshold
    if args.memory_threshold:
        config.alerts.memory_threshold = args.memory_threshold
    
    # Create health checker
    checker = DockerHealthChecker(config)
    
    if args.report:
        # Generate and save report
        report = checker.generate_health_report()
        with open('health_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        print("Health report saved to health_report.json")
    else:
        # Start monitoring
        print(f"{Colors.GREEN}Starting Docker Container Health Checker...{Colors.RESET}")
        print(f"Monitoring interval: {config.monitoring.interval} seconds")
        print(f"Alert thresholds - CPU: {config.alerts.cpu_threshold}%, Memory: {config.alerts.memory_threshold}%")
        print("Press Ctrl+C to stop\n")
        
        checker.monitor_containers()

if __name__ == '__main__':
    main()
