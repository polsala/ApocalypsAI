# Nightly SysGuard

A whimsical system health monitor that reports resource usage with apocalyptic flair and survival-themed alerts.

## Features

- **CPU Monitoring**: Tracks CPU usage and warns when the system is 'overheating'
- **Memory Monitoring**: Monitors RAM usage and alerts when 'running low on supplies'
- **Disk Monitoring**: Watches disk space and warns when 'running out of storage bunkers'
- **Whimsical Alerts**: All warnings come with survival-themed messages
- **Configurable Thresholds**: Customize when alerts trigger
- **JSON Output**: Machine-readable output for integration with other tools

## Installation

```bash
# Clone or copy the script to your system
chmod +x sysguard.sh

# Run directly
./sysguard.sh

# Or add to PATH and run
sysguard
```

## Usage

```bash
# Basic usage with default thresholds
./sysguard.sh

# Custom thresholds (CPU%, Memory%, Disk%)
./sysguard.sh --cpu 80 --memory 90 --disk 85

# JSON output mode
./sysguard.sh --json

# Help
./sysguard.sh --help
```

## Configuration

Edit the script to modify default thresholds:

```bash
DEFAULT_CPU_THRESHOLD=85
DEFAULT_MEMORY_THRESHOLD=90
DEFAULT_DISK_THRESHOLD=80
```

## Output Examples

### Text Mode
```
=== NIGHTLY SYSGUARD SYSTEM STATUS ===

[✓] CPU Usage: 45% (Normal)
[⚠] Memory Usage: 87% (Supplies running low!)
[✓] Disk Usage: 65% (Storage bunkers secure)

Status: System stable. Keep scavenging!
```

### JSON Mode
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "cpu": {
    "usage": 45,
    "status": "normal",
    "message": "CPU running cool"
  },
  "memory": {
    "usage": 87,
    "status": "warning",
    "message": "Supplies running low!"
  },
  "disk": {
    "usage": 65,
    "status": "normal",
    "message": "Storage bunkers secure"
  },
  "overall_status": "warning"
}
```

## Integration

### Cron Job
Add to your crontab for regular monitoring:

```bash
# Check system health every 15 minutes
*/15 * * * * /path/to/sysguard.sh --json >> /var/log/sysguard.log 2>&1
```

### Nagios/Icinga Plugin
Use as a monitoring plugin:

```bash
# Exit codes: 0=OK, 1=WARNING, 2=CRITICAL
./sysguard.sh --check && echo "System OK" || echo "System needs attention"
```

## License

MIT License - feel free to use in your post-apocalyptic survival toolkit!
