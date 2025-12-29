# Nightly Container Health Checker

A whimsical-yet-useful Docker container monitoring tool that keeps your containers healthy and happy. Features real-time resource tracking, customizable alerts, and a dashboard to visualize container wellness.

## Features

- 🏥 Real-time health monitoring of Docker containers
- 📊 Resource usage tracking (CPU, memory, disk, network)
- 🚨 Configurable alert thresholds with multiple notification methods
- 📈 Beautiful ASCII dashboard for container vitals
- 🎨 Color-coded health status indicators
- 📝 Detailed health reports with recommendations
- 🐳 Docker Compose integration

## Installation

### Prerequisites
- Docker
- Python 3.8+

### Quick Start

1. Clone or download this utility
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the health checker:
   ```bash
   python src/main.py
   ```

## Usage

### Basic Monitoring

```bash
# Monitor all running containers
python src/main.py

# Monitor specific containers
python src/main.py --containers web-server db redis

# Set custom alert thresholds
python src/main.py --cpu-threshold 80 --memory-threshold 90
```

### Configuration

Create a `config.yaml` file to customize settings:

```yaml
monitoring:
  interval: 5  # Check every 5 seconds
  containers: []  # Empty means all containers

alerts:
  cpu_threshold: 80
  memory_threshold: 85
  disk_threshold: 90
  network_threshold: 1000  # MB/s

notifications:
  console: true
  file: "health_alerts.log"
  # email: "admin@example.com"
```

### Docker Compose Integration

Add the health checker to your `docker-compose.yml`:

```yaml
services:
  health-checker:
    build: ./nightly-container-health-checker
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./config.yaml:/app/config.yaml
    environment:
      - CONFIG_PATH=/app/config.yaml
```

## Dashboard

The tool provides a real-time ASCII dashboard showing:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           Container Health Dashboard                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ Container: web-server    Status: 🟢 Healthy    CPU: 12.5%    Memory: 256MB    ║
║ Container: database      Status: 🟡 Warning    CPU: 75.2%    Memory: 1.2GB    ║
║ Container: redis         Status: 🔴 Critical   CPU: 95.1%    Memory: 512MB    ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Health Status Indicators

- 🟢 **Healthy**: All metrics within normal ranges
- 🟡 **Warning**: One or more metrics approaching thresholds
- 🔴 **Critical**: Metrics exceed alert thresholds
- ⚪ **Unknown**: Container not found or monitoring error

## Alert Notifications

When thresholds are exceeded, the tool can:

1. Display console warnings with color coding
2. Write alerts to a log file
3. Send email notifications (when configured)
4. Execute custom scripts

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions, please open a GitHub issue or consult the documentation.

---

*Keep your containers healthy, one check at a time! 🐳💚*
