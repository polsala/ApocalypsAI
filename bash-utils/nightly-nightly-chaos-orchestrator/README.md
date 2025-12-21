# Nightly Chaos Orchestrator

A whimsical chaos engineering tool that orchestrates random system failures to test your application's resilience. Inspired by Netflix's Chaos Monkey, but with a post-apocalyptic twist!

## Features

- Randomly kills processes
- Simulates network latency and packet loss
- Randomly fills disk space
- Creates temporary file system errors
- Logs all chaos events for analysis
- Configurable chaos levels (mild, moderate, severe)
- Safety mechanisms to prevent total system destruction

## Installation

```bash
# Clone or download the script
chmod +x chaos_orchestrator.sh
```

## Usage

### Basic Usage

```bash
# Run with default settings (mild chaos)
./chaos_orchestrator.sh

# Run with moderate chaos level
./chaos_orchestrator.sh --level moderate

# Run with severe chaos (use with caution!)
./chaos_orchestrator.sh --level severe

# Run for a specific duration (in seconds)
./chaos_orchestrator.sh --duration 300

# Dry run mode (shows what would happen without actually doing it)
./chaos_orchestrator.sh --dry-run
```

### Configuration

Create a configuration file `chaos_config.env`:

```bash
# Chaos Orchestrator Configuration
CHAOS_LEVEL="moderate"          # mild, moderate, severe
CHAOS_DURATION=600             # Duration in seconds
CHAOS_INTERVAL=60              # Interval between chaos events
ENABLE_PROCESS_CHAOS=true      # Kill random processes
ENABLE_NETWORK_CHAOS=true      # Add network latency
ENABLE_DISK_CHAOS=true         # Fill disk space
ENABLE_FILE_CHAOS=true         # Create file system errors
SAFETY_MODE=true               # Enable safety mechanisms
LOG_FILE="/var/log/chaos_orchestrator.log"
```

## Safety Features

- **Safety Mode**: Prevents killing critical system processes
- **Disk Protection**: Never fills more than 80% of available disk space
- **Network Protection**: Limits network latency to reasonable bounds
- **Process Protection**: Avoids killing essential system services
- **Time Limits**: Automatically stops after specified duration

## Examples

### Testing Web Application Resilience

```bash
# Start your web server in one terminal
./start_web_server.sh

# In another terminal, run chaos engineering
./chaos_orchestrator.sh --level moderate --duration 300

# Monitor your application's response to chaos
```

### CI/CD Pipeline Integration

```bash
# Add to your CI pipeline to test deployment resilience
./chaos_orchestrator.sh --level mild --duration 120

# Check if your application recovered
./health_check.sh
```

## Monitoring and Analysis

The orchestrator logs all chaos events to help you analyze system behavior:

```bash
# View real-time chaos events
tail -f /var/log/chaos_orchestrator.log

# Generate a chaos report
./chaos_orchestrator.sh --report

# Analyze system recovery patterns
./analyze_chaos_impact.sh
```

## Recovery Procedures

After running chaos experiments, use these commands to restore normal operation:

```bash
# Restore network settings
tc qdisc del dev eth0 root 2>/dev/null || true

# Clean up temporary files
find /tmp -name "chaos_*" -delete

# Restart any killed services (if safe)
./restart_critical_services.sh
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add new chaos scenarios
4. Test thoroughly
5. Submit a pull request

## License

This tool is provided as-is for educational and testing purposes. Use at your own risk!

## Disclaimer

⚠️ **WARNING**: This tool is designed to cause system disruption. Only use it in controlled environments like:

- Development servers
- Testing environments
- Virtual machines
- Containerized environments

**NEVER** use this tool on:

- Production systems
- Critical infrastructure
- Systems with important data
- Shared environments without permission

The authors are not responsible for any damage caused by misuse of this tool.
