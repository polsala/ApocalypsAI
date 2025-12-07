# Nightly Rust Chaos Chaos Chaos

A blazing-fast Rust CLI tool that orchestrates multiple chaos engineering attacks across your system with precise control and safety limits.

## Features

- **Network Chaos**: Introduce latency, packet loss, and bandwidth limits
- **CPU Chaos**: Spike CPU usage with configurable intensity
- **Memory Chaos**: Consume memory with safety limits
- **Service Chaos**: Restart or stop services
- **Time Chaos**: Manipulate system time
- **Safety First**: Built-in safeguards and rollback mechanisms

## Installation

### From Crates.io
```bash
# Not yet published - build from source for now
```

### From Source
```bash
# Clone the repository
git clone <repo-url>
cd nightly-rust-chaos-chaos-chaos

# Build with optimizations
cargo build --release

# Install to PATH
cargo install --path .
```

### Pre-built Binaries
Download the appropriate binary for your platform from the releases page and add it to your PATH.

## Usage

### Basic Commands

```bash
# Show help
chaos-chaos-chaos --help

# List available chaos scenarios
chaos-chaos-chaos list-scenarios

# Run a specific chaos scenario
chaos-chaos-chaos run --scenario network-latency --duration 30s

# Run chaos with custom parameters
chaos-chaos-chaos run --scenario cpu-spike --duration 60s --intensity 80

# Run multiple scenarios sequentially
chaos-chaos-chaos run --scenario network-latency --scenario memory-usage --duration 30s

# Run chaos in the background
chaos-chaos-chaos run --scenario cpu-spike --duration 300s --background

# Check chaos status
chaos-chaos-chaos status

# Stop all running chaos
chaos-chaos-chaos stop
```

### Advanced Usage

```bash
# Dry run (simulate without actual chaos)
chaos-chaos-chaos run --scenario network-latency --duration 30s --dry-run

# Verbose output
chaos-chaos-chaos run --scenario cpu-spike --duration 60s --verbose

# Custom configuration file
chaos-chaos-chaos run --config /path/to/config.yaml

# Run with rollback on failure
chaos-chaos-chaos run --scenario service-restart --rollback-on-failure

# Monitor system metrics during chaos
chaos-chaos-chaos run --scenario memory-usage --monitor
```

### Scenario Examples

#### Network Chaos
```bash
# Add 100ms latency to all network traffic
chaos-chaos-chaos run --scenario network-latency --latency 100ms --duration 60s

# Introduce 10% packet loss
chaos-chaos-chaos run --scenario network-loss --loss 10% --duration 30s

# Limit bandwidth to 1Mbps
chaos-chaos-chaos run --scenario network-bandwidth --bandwidth 1mbps --duration 120s
```

#### CPU Chaos
```bash
# Spike CPU usage to 80% for 2 minutes
chaos-chaos-chaos run --scenario cpu-spike --intensity 80 --duration 120s

# Gradual CPU ramp
chaos-chaos-chaos run --scenario cpu-ramp --start-intensity 20 --end-intensity 90 --ramp-duration 60s
```

#### Memory Chaos
```bash
# Consume 2GB of memory
chaos-chaos-chaos run --scenario memory-usage --memory 2gb --duration 300s

# Gradual memory consumption
chaos-chaos-chaos run --scenario memory-ramp --start-memory 512mb --end-memory 4gb --ramp-duration 120s
```

#### Service Chaos
```bash
# Restart a specific service
chaos-chaos-chaos run --scenario service-restart --service nginx --duration 10s

# Stop a service temporarily
chaos-chaos-chaos run --scenario service-stop --service apache2 --duration 30s
```

#### Time Chaos
```bash
# Shift system time forward by 1 hour
chaos-chaos-chaos run --scenario time-shift --offset +1h --duration 60s

# Random time jumps
chaos-chaos-chaos run --scenario time-jump --max-offset 30m --duration 180s
```

## Configuration

Create a `chaos.yaml` configuration file:

```yaml
# chaos.yaml
safety:
  max_duration: 300s
  max_cpu_intensity: 90
  max_memory_usage: 8gb
  allowed_interfaces: ["eth0", "wlan0"]
  protected_services: ["sshd", "systemd"]

scenarios:
  network-latency:
    default_duration: 60s
    default_latency: 50ms
  cpu-spike:
    default_duration: 120s
    default_intensity: 70
  memory-usage:
    default_duration: 300s
    default_memory: 2gb
```

## Safety Features

- **Duration Limits**: Prevents chaos from running indefinitely
- **Resource Limits**: Caps CPU and memory usage to prevent system lockup
- **Protected Services**: Prevents stopping critical system services
- **Rollback Mechanisms**: Automatic cleanup on failure or timeout
- **Dry Run Mode**: Test scenarios without actual impact

## Monitoring

The tool provides real-time monitoring capabilities:

```bash
# Monitor during chaos execution
chaos-chaos-chaos run --scenario cpu-spike --monitor

# View system metrics
chaos-chaos-chaos metrics

# Export metrics to file
chaos-chaos-chaos metrics --export /path/to/metrics.json
```

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid arguments
- `3`: Safety limit exceeded
- `4`: Permission denied
- `5`: Chaos execution failed
- `6`: Rollback failed

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

⚠️ **Use at your own risk!** This tool is designed for chaos engineering in controlled environments. Never use it on production systems without proper safeguards and approvals.

The authors are not responsible for any damage caused by misuse of this tool.

## Support

- Report bugs via [GitHub Issues](https://github.com/polsala/ApocalypsAI/issues)
- Join our [Discord](https://discord.gg/example) for community support
- Check the [Wiki](https://github.com/polsala/ApocalypsAI/wiki) for documentation

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

---

**Remember**: With great power comes great responsibility. Use chaos engineering to build more resilient systems, not to break things!
