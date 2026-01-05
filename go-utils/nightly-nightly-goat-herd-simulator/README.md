# Goat Herd Simulator

A whimsical concurrent goat herd simulator written in Go. It models a herd of goats that graze, reproduce, and occasionally cause playful chaos. Perfect for stress-testing concurrent programming concepts or just having fun with animal simulations.

## Features
- Concurrent goat agents using goroutines
- Grazing, reproduction, and mischief behaviors
- Configurable herd size and simulation duration
- Colored terminal output showing the herd state
- Deterministic tests with mocked randomness

## Usage
```bash
# Run the simulation with default settings
./goat-herd-simulator

# Customize herd size and duration
./goat-herd-simulator --herd-size 50 --duration 30s

# Run with verbose logging
./goat-herd-simulator --verbose
```

## Build
```bash
go build -o goat-herd-simulator main.go
```

## Testing
Run the included tests to verify deterministic behavior:
```bash
go test ./...
```

## Example Output
```
[INFO] Starting simulation with 10 goats for 15s
[GOAT] Billy is grazing...
[GOAT] Daisy reproduced! A new kid joined the herd.
[GOAT] Rocky caused a minor stampede!
[INFO] Simulation ended. Final herd size: 12 goats.
```

## License
MIT
