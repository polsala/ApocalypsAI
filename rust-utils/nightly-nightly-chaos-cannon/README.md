# Nightly Chaos Cannon

A whimsical CLI tool that injects controlled chaos into your local development environment to test resilience and build muscle memory for real-world outages.

## Features

- **Network Chaos**: Drop packets, add latency, and simulate bandwidth throttling
- **Process Chaos**: Kill processes, freeze them, or make them unresponsive
- **Disk Chaos**: Fill disks, corrupt files, and simulate I/O errors
- **Memory Chaos**: Consume memory to trigger OOM conditions
- **Whimsical Mode**: Randomly inject chaos with a touch of humor

## Installation

### Prerequisites
- Linux or macOS (Windows support is not implemented)
- `sudo` privileges for network and disk operations

### Build from Source

```bash
# Clone the repository
git clone <repo-url>
cd nightly-chaos-cannon

# Build the project
cargo build --release

# Install the binary (optional)
sudo cp target/release/chaos-cannon /usr/local/bin/
```

## Usage

### Basic Commands

```bash
# Show help
chaos-cannon --help

# Inject network latency
chaos-cannon network latency --interface lo --delay 100ms --jitter 10ms

# Kill a process by name
chaos-cannon process kill --name firefox

# Fill disk space
chaos-cannon disk fill --path /tmp --size 100MB

# Consume memory
chaos-cannon memory consume --size 512MB

# Whimsical chaos
chaos-cannon whimsical --target all
```

### Advanced Usage

```bash
# Add packet loss
chaos-cannon network loss --interface lo --percent 10

# Freeze a process
chaos-cannon process freeze --name nginx

# Corrupt a file
chaos-cannon disk corrupt --path /tmp/test.txt

# Simulate I/O errors
chaos-cannon disk io-error --path /tmp/test.txt
```

### Cleanup

```bash
# Remove network rules
chaos-cannon cleanup network --interface lo

# Kill all chaos processes
chaos-cannon cleanup processes

# Remove disk chaos files
chaos-cannon cleanup disk --path /tmp
```

## Safety Notes

- This tool is designed for local development environments only
- Use with caution and always clean up after testing
- Some operations require root privileges
- The whimsical mode is unpredictable by design

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
