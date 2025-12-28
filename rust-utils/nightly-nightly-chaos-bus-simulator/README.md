# Nightly Chaos Bus Simulator

A whimsical CLI tool that simulates a chaotic bus system with random events, delays, and passenger interactions. Perfect for testing resilience, generating chaos for fun, or just watching the madness unfold.

## Features

- 🚌 Simulate multiple bus routes with random events
- 🎲 Chaotic events: traffic jams, weather delays, passenger strikes
- 📊 Real-time statistics and chaos metrics
- 🎨 Colorful terminal output with ASCII art
- 🎯 Configurable chaos levels and simulation duration
- 📈 Export simulation results to JSON

## Installation

### From Source (Rust)

```bash
# Clone the repository
# Navigate to the chaos-bus-simulator directory
# Build and install
cargo build --release

# Run the simulator
./target/release/nightly-chaos-bus-simulator
```

### Usage

```bash
# Basic simulation
nightly-chaos-bus-simulator

# Custom chaos level (1-10)
nightly-chaos-bus-simulator --chaos-level 8

# Custom duration in seconds
nightly-chaos-bus-simulator --duration 60

# Export results to JSON
nightly-chaos-bus-simulator --export results.json

# View help
nightly-chaos-bus-simulator --help
```

## Configuration

The simulator accepts the following command-line arguments:

- `--chaos-level`: Chaos intensity (1-10, default: 5)
- `--duration`: Simulation duration in seconds (default: 30)
- `--routes`: Number of bus routes (default: 3)
- `--buses-per-route`: Number of buses per route (default: 2)
- `--export`: Export path for JSON results

## Example Output

```
🚌 Chaos Bus Simulator Starting...

Route 1: Downtown Express
  🚍 Bus 1: On time
  🚍 Bus 2: Delayed (Traffic jam)

Route 2: Airport Shuttle
  🚍 Bus 1: On time
  🚍 Bus 2: On time

Route 3: University Loop
  🚍 Bus 1: Delayed (Student protest)
  🚍 Bus 2: On time

Chaos Level: 7/10
Total Delays: 2
Active Buses: 6
```

## Why Use This?

- **Testing Resilience**: Test how your systems handle chaotic inputs
- **Team Building**: Fun way to discuss chaos engineering principles
- **Stress Relief**: Watch the chaos unfold when you need a break
- **Learning**: Understand how small disruptions cascade through systems

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Chaos Events

The simulator includes various chaotic events:

- Traffic jams
- Weather delays (rain, snow, fog)
- Passenger strikes
- Mechanical failures
- Route detours
- Fuel shortages
- Driver strikes
- Construction delays

May the chaos be ever in your favor! 🎲🚌
