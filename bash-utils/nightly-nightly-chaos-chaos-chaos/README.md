# nightly-chaos-chaos-chaos

A whimsical chaos-engineering orchestrator that injects controlled mayhem into local services via Bash.

## Features
- Randomly kill or restart services.
- Simulate network latency and packet loss.
- Simulate CPU load spikes.
- Log chaos events for later review.
- Dry-run mode for safe rehearsals.

## Requirements
- Bash 4+
- `systemctl` (optional)
- `tc` (optional, for network chaos)
- `stress` (optional, for CPU chaos)

## Usage
```bash
# Dry-run (safe)
./src/main.sh --dry-run

# Execute chaos
./src/main.sh --execute

# View chaos log
./src/main.sh --log

# Reset network and CPU state
./src/main.sh --reset
```

## License
MIT
