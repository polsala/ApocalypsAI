# Nightly Chaos Orchestrator

A whimsical chaos engineering tool that injects controlled mayhem into systems to test resilience. Perfect for ensuring your infrastructure can handle the apocalypse!

## Features

- **Network Chaos**: Randomly drop packets, add latency, or corrupt data
- **Resource Chaos**: Consume CPU, memory, or disk space
- **Service Chaos**: Restart, kill, or freeze services
- **Time Chaos**: Manipulate system time or create time loops
- **Random Chaos**: Completely unpredictable mayhem

## Installation

```bash
# Clone or download the chaos_orchestrator.sh script
chmod +x chaos_orchestrator.sh
```

## Usage

### Basic Chaos

```bash
# Run a quick chaos scenario
./chaos_orchestrator.sh --scenario network --duration 30s

# Run resource chaos with custom parameters
./chaos_orchestrator.sh --scenario resource --cpu 80 --memory 50 --duration 1m

# Run service chaos on specific services
./chaos_orchestrator.sh --scenario service --services nginx,redis --action restart
```

### Advanced Chaos

```bash
# Run multiple scenarios in sequence
./chaos_orchestrator.sh --scenario network,resource --duration 2m

# Run with custom chaos parameters
./chaos_orchestrator.sh --scenario network --latency 100ms --packet-loss 10% --corruption 5%

# Run random chaos for maximum unpredictability
./chaos_orchestrator.sh --scenario random --duration 5m
```

### Monitoring and Reporting

```bash
# Generate a chaos report
./chaos_orchestrator.sh --scenario network --duration 30s --report

# View chaos history
./chaos_orchestrator.sh --history

# Clean up chaos artifacts
./chaos_orchestrator.sh --cleanup
```

## Scenarios

### Network Chaos

Simulates network issues:
- Packet loss
- Latency injection
- Bandwidth throttling
- Packet corruption

### Resource Chaos

Consumes system resources:
- CPU stress
- Memory consumption
- Disk I/O stress
- Disk space consumption

### Service Chaos

Manipulates running services:
- Service restart
- Service kill
- Service freeze
- Service overload

### Time Chaos

Manipulates system time:
- Time acceleration
- Time deceleration
- Time jumps
- Time loops

### Random Chaos

Completely unpredictable chaos that combines multiple scenarios.

## Safety Features

- **Time Limits**: All chaos has maximum duration limits
- **Resource Guards**: Prevents system from becoming completely unusable
- **Rollback Mechanisms**: Automatic cleanup after chaos ends
- **Monitoring**: Real-time system health monitoring

## Examples

### Quick Network Test

```bash
# Test network resilience with 10% packet loss for 1 minute
./chaos_orchestrator.sh --scenario network --packet-loss 10% --duration 1m
```

### CPU Stress Test

```bash
# Stress test CPU at 90% for 5 minutes
./chaos_orchestrator.sh --scenario resource --cpu 90 --duration 5m
```

### Service Resilience Test

```bash
# Restart web services every 30 seconds for 2 minutes
./chaos_orchestrator.sh --scenario service --services nginx,apache --action restart --interval 30s --duration 2m
```

## Contributing

1. Fork the repository
2. Create a new chaos scenario
3. Add tests for your scenario
4. Submit a pull request

## License

MIT License - Use at your own risk. Chaos may cause unexpected behavior!

## Disclaimer

This tool is for testing and educational purposes only. Use responsibly and only on systems you have permission to test. The authors are not responsible for any damage caused by this tool.

## Changelog

- v1.0.0: Initial release with network, resource, service, and time chaos
- v1.1.0: Added random chaos scenario and improved safety features
- v1.2.0: Added comprehensive reporting and monitoring capabilities
