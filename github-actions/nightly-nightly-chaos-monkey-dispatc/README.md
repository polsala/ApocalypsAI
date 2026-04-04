# nightly-chaos-monkey-dispatcher

A whimsical yet practical GitHub Action that injects random failures into your CI pipeline—perfect for stress-testing workflows.

## Features

- Randomly skips steps or jobs
- Simulates network delays or outages
- Fails builds with configurable probability
- Logs all chaos events for post-mortem analysis

## Usage

Add this step in any job:

```yaml
- name: Invoke Chaos Monkey
  uses: polsala/ApocalypsAI/utils/nightly-chaos-monkey-dispatcher@main
  with:
    failure_rate: 0.3
    delay_max_seconds: 5
```

### Inputs

| Input               | Description                          | Default |
|---------------------|--------------------------------------|---------|
| `failure_rate`      | Chance of inducing a failure (0–1)   | `0.1`   |
| `delay_max_seconds` | Max delay to simulate latency (sec)  | `3`     |

## License
MIT
