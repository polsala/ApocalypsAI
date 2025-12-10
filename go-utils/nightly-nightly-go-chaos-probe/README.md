# Nightly Go Chaos Probe

A whimsical-yet-useful Go utility for testing network resilience by simulating latency, packet loss, and jitter. Perfect for chaos engineering experiments and testing how your applications handle network degradation.

## Features

- Simulate network latency with configurable delay
- Introduce packet loss with random drop rates
- Add jitter (random variation in latency)
- Works with both local and remote services
- Simple CLI interface with real-time statistics
- Whimsical status messages to keep you entertained during chaos

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd nightly-go-chaos-probe

# Build the utility
go build -o chaos-probe src/main.go

# Or run directly
go run src/main.go
```

## Usage

```bash
# Basic usage - test google.com with 100ms latency
./chaos-probe --target google.com --latency 100

# Advanced usage - simulate packet loss and jitter
./chaos-probe --target api.example.com --latency 200 --packet-loss 10 --jitter 50

# Test local service
./chaos-probe --target localhost:8080 --latency 50 --packet-loss 5

# View help
./chaos-probe --help
```

## Options

- `--target`: Target host:port or hostname to test (required)
- `--latency`: Fixed latency in milliseconds (default: 0)
- `--packet-loss`: Packet loss percentage (0-100, default: 0)
- `--jitter`: Jitter in milliseconds (random variation around latency, default: 0)
- `--requests`: Number of requests to make (default: 10)
- `--timeout`: Request timeout in milliseconds (default: 5000)

## Example Output

```
🧪 Initiating chaos probe...
🎯 Target: google.com:80
⚡ Latency: 100ms ± 50ms jitter
💔 Packet loss: 10%
📡 Making 10 requests...

Request 1: 145ms ✅ (The network gods are smiling today!)
Request 2: 203ms ✅ (Smooth sailing!)
Request 3: ❌ DROPPED (The network gremlins got this one)
Request 4: 98ms ✅ (Lightning fast!)

📊 Statistics:
- Success rate: 75.0%
- Average latency: 148.7ms
- Min latency: 98ms
- Max latency: 203ms
- Total requests: 10
- Failed requests: 3

🎉 Chaos probe complete! Your service survived... mostly.
```

## Use Cases

- **Chaos Engineering**: Test how your application handles network degradation
- **Load Testing**: Simulate real-world network conditions
- **Development**: Test timeout handling and retry logic
- **Monitoring**: Verify alert thresholds under stress
- **Training**: Teach teams about network reliability

## Safety Notes

- This tool is for testing and educational purposes
- Use responsibly in development/staging environments
- Avoid using on production systems without proper safeguards
- The whimsical messages are optional but highly recommended for team morale

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is designed to help you build more resilient systems. Use it wisely, and remember: with great power comes great responsibility (and sometimes hilarious error messages).
