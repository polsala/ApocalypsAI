# nightly-chaos-monkey-scheduler

A whimsical yet practical GitHub Action that injects controlled chaos into your systems by scheduling random disruptions during off-peak hours.

## Features

- Randomly schedules chaos events based on configured probabilities
- Respects business hour boundaries to avoid disruptions
- Logs all scheduled events for auditability
- Dry-run mode for testing configurations

## Usage

```yaml
name: Schedule Chaos Monkey
on:
  schedule:
    - cron: '0 2 * * *' # Run daily at 2 AM UTC
jobs:
  schedule-chaos:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      - name: Schedule Chaos Event
        uses: polsala/ApocalypsAI/utils/nightly-chaos-monkey-scheduler@main
        with:
          probability: 0.3
          start_hour: 22
          end_hour: 6
          dry_run: false
```

### Inputs

| Input         | Description                                  | Default |
|---------------|----------------------------------------------|---------|
| `probability` | Likelihood of scheduling an event (0.0 - 1.0) | 0.5     |
| `start_hour`  | Start of off-peak window (24-hour format)    | 22      |
| `end_hour`    | End of off-peak window (24-hour format)      | 6       |
| `dry_run`     | If true, log event without actually scheduling| false   |

## License

MIT
