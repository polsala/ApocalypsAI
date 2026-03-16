# nightly-chaos-monkey-scheduler

A playful Bash utility that schedules randomized chaos events—like service restarts or network hiccups—to help engineers test system resilience in development environments.

## Features

- Schedule random disruptions (services, network, disk I/O)
- Dry-run mode to preview actions
- Configurable disruption frequency
- Safe defaults: only affects local machine

## Usage

```bash
./src/chaos_monkey.sh start --interval=10s
```

Options:
- `--interval=<duration>`: Set delay between disruptions (default: 30s)
- `--dry-run`: Preview disruptions without executing them
- `--help`: Show help message

## Examples

Start chaos monkey with default settings:

```bash
./src/chaos_monkey.sh start
```

Preview disruptions every 5 seconds:

```bash
./src/chaos_monkey.sh start --interval=5s --dry-run
```

Stop the chaos:

```bash
./src/chaos_monkey.sh stop
```

## Requirements

- Bash 4+
- Linux/macOS compatible commands (`systemctl`, `tc`, `dd`)

⚠️ Warning: For testing/dev use only. Not recommended for production systems.
