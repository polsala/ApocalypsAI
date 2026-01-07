# Nightly Docker Chaos Monkey

A whimsical-yet-useful containerized chaos engineering tool that randomly injects failures into Docker environments for resilience testing.

## Features

- **Random failure injection**: CPU spikes, memory pressure, network latency, container kills
- **Configurable chaos**: Set intensity levels and target containers
- **Safe defaults**: Only affects containers with `chaos.monkey=true` label
- **Real-time monitoring**: Live dashboard showing chaos events
- **Self-healing**: Automatically recovers after chaos injection

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose

### Basic Usage

1. **Label your containers for chaos testing**:

```bash
# Start a container with chaos monkey enabled
docker run -d --label "chaos.monkey=true" --name test-app nginx:latest
```

2. **Run the chaos monkey**:

```bash
# Run chaos monkey for 5 minutes with medium intensity
docker run --rm --name chaos-monkey \
  --network host \
  --volume /var/run/docker.sock:/var/run/docker.sock \
  ghcr.io/polsala/nightly-docker-chaos-monkey:latest \
  --duration 300 \
  --intensity medium
```

### Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  chaos-monkey:
    image: ghcr.io/polsala/nightly-docker-chaos-monkey:latest
    container_name: chaos-monkey
    network_mode: host
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - CHAOS_DURATION=600
      - CHAOS_INTENSITY=high
      - CHAOS_INTERVAL=30
    restart: unless-stopped

  test-app:
    image: nginx:latest
    container_name: test-app
    labels:
      - "chaos.monkey=true"
    ports:
      - "8080:80"
```

Start the chaos environment:

```bash
docker-compose up -d
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CHAOS_DURATION` | `300` | Duration in seconds to run chaos (0 = infinite) |
| `CHAOS_INTENSITY` | `medium` | Intensity level: `low`, `medium`, `high` |
| `CHAOS_INTERVAL` | `60` | Interval in seconds between chaos events |
| `CHAOS_TARGET_LABEL` | `chaos.monkey=true` | Docker label to identify target containers |
| `CHAOS_NETWORK_DELAY` | `100` | Network delay in milliseconds for latency injection |
| `CHAOS_MEMORY_PRESSURE` | `50` | Memory pressure percentage (0-100) |
| `CHAOS_CPU_STRESS` | `80` | CPU stress percentage (0-100) |

### Command Line Options

```bash
--duration SECONDS    Duration to run chaos (0 = infinite)
--intensity LEVEL      Intensity: low, medium, high
--interval SECONDS   Interval between events
--target-label LABEL Docker label to target
--network-delay MS   Network delay in milliseconds
--memory-pressure %  Memory pressure percentage
--cpu-stress %       CPU stress percentage
--dry-run           Show what would happen without executing
--help              Show help message
```

## Chaos Events

The chaos monkey randomly selects from these failure modes:

1. **Container Kill**: Randomly kills target containers
2. **CPU Spike**: Spikes CPU usage to cause load
3. **Memory Pressure**: Consumes memory to cause OOM conditions
4. **Network Latency**: Adds artificial network delay
5. **Disk I/O**: Creates disk I/O pressure
6. **Random Restart**: Restarts containers unexpectedly

## Safety Features

- **Label-based targeting**: Only affects containers with the chaos.monkey label
- **Graceful degradation**: Respects container restart policies
- **Resource limits**: Never exceeds configured intensity levels
- **Monitoring**: Logs all chaos events for analysis

## Monitoring

The chaos monkey logs all events to stdout in JSON format:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "event": "container_kill",
  "target": "test-app",
  "intensity": "medium",
  "success": true
}
```

## Development

### Building the Image

```bash
docker build -t nightly-docker-chaos-monkey:latest .
```

### Running Tests

```bash
docker-compose -f docker-compose.test.yml up --build
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new chaos events
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

⚠️ **Use at your own risk!** This tool is designed to cause failures. Only use in development and testing environments. Never run in production without proper safeguards.

## Support

- Report issues on GitHub
- Join our Discord for community support
- Check the wiki for advanced configuration
