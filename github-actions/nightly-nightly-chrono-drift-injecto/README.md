# Nightly Chrono-Drift Injector

## Whimsical Purpose
In the ever-shifting temporal landscape of the ApocalypsAI, even our workflows can experience subtle 'chrono-drift'. This utility, the `Chrono-Drift Injector`, is designed to intentionally introduce minor temporal anomalies (delays) and occasional reality glitches (failures) into your GitHub Actions workflows. Why? To ensure our systems are robust enough to withstand the universe's inherent unpredictability, and to expose those pesky, timing-sensitive bugs that only appear when the stars align just wrong.

## Practical Usefulness
This GitHub Action is a light-touch chaos engineering tool for your CI/CD pipelines. By injecting controlled, randomized delays and transient failures, it helps you:

- **Identify Race Conditions**: Uncover parts of your code or infrastructure that depend on strict timing, which might pass locally but fail intermittently in CI.
- **Detect Brittle Dependencies**: Pinpoint services or components that are not resilient to network latency or temporary unavailability.
- **Improve Timeout Handling**: Ensure your applications and tests gracefully handle delays and timeouts.
- **Enhance Workflow Robustness**: Build more resilient CI/CD pipelines that can recover from or report on unexpected transient issues.

## How it Works
The action executes a simple bash script that:
1. Calculates a random delay within a specified range (min_delay to max_delay).
2. Pauses the workflow step for that calculated duration.
3. With a configurable probability (failure_chance), it may cause the step to fail.

An optional `drift_seed` can be provided to make the 'randomness' reproducible for debugging specific scenarios.

## Usage
Add this action as a step in any of your GitHub Actions jobs. It's recommended to use it strategically, perhaps in a dedicated 'flakiness test' job or before critical deployment steps to ensure resilience.

```yaml
name: CI with Chrono-Drift
on: [push, workflow_dispatch]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Inject a little temporal instability
        uses: polsala/ApocalypsAI/utils/nightly-chrono-drift-injector@main # Replace 'main' with your branch/tag if needed
        with:
          min_delay: 2
          max_delay: 10
          failure_chance: 5 # 5% chance to fail
          # drift_seed: '42' # Uncomment for reproducible drift

      - name: Run tests (after potential drift)
        run: |
          echo "Running tests..."
          # Your actual test commands here
          # For example: npm test or cargo test
          sleep 1 # Simulate some work
          echo "Tests completed."

      - name: Another step, unaffected by previous drift
        run: echo "This step runs regardless of previous drift, unless it failed."
```

## Inputs
| Input          | Description                                                               | Required | Default |
|----------------|---------------------------------------------------------------------------|----------|---------|
| `min_delay`    | Minimum delay in seconds to inject.                                       | `false`  | `0`     |
| `max_delay`    | Maximum delay in seconds to inject.                                       | `false`  | `5`     |
| `failure_chance`| Percentage chance (0-100) for the step to fail.                           | `false`  | `0`     |
| `drift_seed`   | Optional seed for reproducible randomness. If not provided, uses current timestamp. | `false`  | `''`    |

## Outputs
None.

## Development & Testing
See `src/drift_injector.sh` for the core logic and `tests/test_drift_injector.sh` for the self-contained, deterministic test suite.
