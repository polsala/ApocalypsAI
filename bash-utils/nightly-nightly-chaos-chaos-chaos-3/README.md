# Nightly Chaos Chaos Chaos

A whimsical chaos engineering toolkit that injects controlled mayhem into systems via configurable failure modes.

## Features
- Network latency injection
- Service disruption
- Resource exhaustion
- Random chaos
- Time manipulation
- Cleanup automation

## Usage
```bash
./src/main.sh --mode network --duration 30s
./src/main.sh --mode service --service-name nginx
./src/main.sh --mode resource --cpu-cores 2 --memory-mb 512
./src/main.sh --mode random
./src/main.sh --mode time --offset "+1 hour"
./src/main.sh --cleanup
```

## Requirements
- Linux with systemd
- tc (traffic control)
- stress (for resource exhaustion)

## License
MIT
