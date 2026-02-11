# nightly-chaos-monkey-scheduler

A lightweight bash utility that schedules and executes chaos experiments such as network delays, packet loss, or service restarts on Linux systems.

## Features

- Schedule chaos events via cron-style syntax
- Supports network disruptions (using `tc`)
- Supports service restarts (using `systemctl`)
- Dry-run mode for validation
- Self-contained and portable

## Usage

```bash
# Schedule a network delay of 1000ms every hour
./chaos-monkey-scheduler.sh --type network --delay 1000 --interval '@hourly'

# Restart nginx service daily at 2AM
./chaos-monkey-scheduler.sh --type service --service nginx --interval '0 2 * * *'

# Dry run to validate configuration
./chaos-monkey-scheduler.sh --type network --delay 500 --interval '@daily' --dry-run
```

## Requirements

- Linux OS with `tc`, `systemctl`, and `crontab`
- Root or sufficient privileges for network/service manipulation

## License

MIT
