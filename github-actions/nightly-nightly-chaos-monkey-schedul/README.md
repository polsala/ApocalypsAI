# nightly-chaos-monkey-scheduler

A whimsical yet powerful GitHub Action that introduces controlled chaos into your workflows—because even in apocalypse times, systems need stress-tested resilience.

## Features

- Schedule random or targeted failures during CI runs
- Supports service disruption, network latency, and resource exhaustion
- Fully configurable via YAML
- Safe by design – won't affect production unless explicitly allowed

## Usage

Create `.github/workflows/chaos-test.yml`:

```yaml
name: Chaos Test
on: [push]
jobs:
  chaos:
    runs-on: ubuntu-latest
    steps:
      - name: Inject Chaos
        uses: polsala/ApocalypsAI/utils/nightly-chaos-monkey-scheduler@main
        with:
          mode: 'network-delay'
          duration: '5s'
          target-service: 'webapp'
```

### Inputs

| Input           | Description                      | Default     |
|----------------|----------------------------------|-------------|
| `mode`         | Type of chaos to simulate        | `random`    |
| `duration`     | How long the chaos should last   | `10s`       |
| `target-service` | Optional service filter       | N/A         |

## License
MIT
