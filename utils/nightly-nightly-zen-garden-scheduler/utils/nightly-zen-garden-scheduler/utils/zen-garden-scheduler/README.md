# Zen Garden Scheduler

A whimsical utility that creates a calming daily schedule from a simple YAML configuration. Perfect for community members who want structured breaks.

## Features

- Reads a list of activities with durations.
- Generates a timeline starting at 09:00.
- Outputs plain‑text schedule.

## Usage

```sh
python -m zen_garden_scheduler --config schedule.yaml
```

`schedule.yaml` example:

```yaml
activities:
  - name: Meditation
    duration: 15
  - name: Tea Break
    duration: 10
  - name: Light Reading
    duration: 20
```

Will output:

```
09:00 - 09:15: Meditation
09:15 - 09:25: Tea Break
09:25 - 09:45: Light Reading
```

## Implementation

- Pure Python 3.11, only `pyyaml` optional.
- Deterministic, no external calls.
