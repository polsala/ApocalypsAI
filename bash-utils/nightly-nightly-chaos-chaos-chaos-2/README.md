# Nightly Chaos Chaos Chaos

A whimsical yet practical chaos engineering tool that injects controlled chaos into your systems to test resilience. Inspired by the chaos of post-apocalyptic wastelands, this tool helps you build systems that can survive anything!

## Features

- **Network Chaos**: Introduce latency, packet loss, and bandwidth throttling
- **Resource Chaos**: Spike CPU and memory usage
- **Service Chaos**: Randomly restart or stop services
- **Time Chaos**: Manipulate system time
- **Cleanup**: Automatically restore your system to its original state

## Installation

1. Clone or copy the `src/main.sh` script to your system
2. Ensure you have the required dependencies installed:
   - `tc` (Traffic Control) for network chaos
   - `stress` for resource chaos
   - `systemctl` for service chaos
   - Root privileges (sudo) for most operations

## Usage

### Basic Chaos

```bash
# Inject network latency of 100ms
./src/main.sh network latency 100ms

# Add 10% packet loss
./src/main.sh network packet-loss 10%

# Throttle bandwidth to 1Mbps
./src/main.sh network bandwidth 1Mbps

# Spike CPU usage to 80%
./src/main.sh resource cpu 80

# Consume 50% of available memory
./src/main.sh resource memory 50

# Restart a service randomly
./src/main.sh service restart apache2

# Stop a service randomly
./src/main.sh service stop nginx

# Shift system time forward by 1 hour
./src/main.sh time shift +1h
```

### Advanced Chaos

```bash
# Combine multiple chaos types
./src/main.sh network latency 200ms && ./src/main.sh resource cpu 90

# Run chaos for a specific duration
./src/main.sh network latency 100ms --duration 300  # 5 minutes

# List all available chaos types
./src/main.sh help
```

### Cleanup

```bash
# Restore network settings
./src/main.sh cleanup network

# Restore all chaos effects
./src/main.sh cleanup all
```

## Safety Features

- **Dry Run Mode**: Test your chaos commands before executing them
- **Automatic Cleanup**: Built-in mechanisms to restore your system
- **Logging**: Detailed logs of all chaos operations
- **Validation**: Checks for required dependencies and permissions

## Examples

### Testing Web Application Resilience

```bash
# Simulate poor network conditions while testing your web app
./src/main.sh network latency 150ms
./src/main.sh network packet-loss 5%

# Run your tests here...

# Clean up
./src/main.sh cleanup network
```

### Testing Database Failover

```bash
# Stop the primary database service
./src/main.sh service stop mysql

# Wait for failover to occur
sleep 30

# Restart the service
./src/main.sh service restart mysql

# Clean up
./src/main.sh cleanup
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

Use this tool responsibly and only in controlled environments. The authors are not responsible for any damage caused by misuse of this tool.

## Acknowledgments

- Inspired by the chaos of post-apocalyptic wastelands
- Built for the brave souls testing system resilience
- Part of the ApocalypsAI Nightly Integrator collection
