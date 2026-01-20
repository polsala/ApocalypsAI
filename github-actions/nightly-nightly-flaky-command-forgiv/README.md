# Nightly Flaky Command Forgiver

A GitHub Action that automatically retries a command or script a specified number of times upon failure, with an optional delay between attempts. Perfect for dealing with transient network issues, flaky tests, or unreliable external services in your CI/CD workflows.

## Usage

Add this action to your workflow to wrap any command or script that might occasionally fail.

```yaml
name: Example Workflow with Flaky Command Forgiver
on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies (might be flaky)
        uses: ./github-actions/nightly-flaky-command-forgiver
        with:
          command: 'npm install --force' # Example of a potentially flaky command
          max_retries: 3
          delay_seconds: 10 # Wait 10 seconds before retrying

      - name: Run flaky test suite
        id: flaky_tests
        uses: ./github-actions/nightly-flaky-command-forgiver
        with:
          command: |
            # Simulate a command that fails twice then succeeds
            RETRY_FILE=".flaky_test_counter"
            CURRENT_ATTEMPT=$(cat $RETRY_FILE || echo 0)
            echo "Running test suite attempt: $((CURRENT_ATTEMPT + 1))"
            echo $((CURRENT_ATTEMPT + 1)) > $RETRY_FILE
            if [ "$CURRENT_ATTEMPT" -lt 2 ]; then
              echo "Test suite failed (simulated)."
              exit 1
            else
              echo "Test suite passed (simulated)."
              exit 0
          max_retries: 2 # Total 3 attempts (initial + 2 retries)
          delay_seconds: 5

      - name: Check flaky test outcome
        if: steps.flaky_tests.outputs.outcome == 'success'
        run: echo "Flaky tests eventually passed!"
      - name: Handle permanent flaky test failure
        if: steps.flaky_tests.outputs.outcome == 'failure'
        run: echo "Flaky tests failed permanently after retries. Investigate!" && exit 1
```

### Inputs

| Name            | Description                                                               |
|-----------------|---------------------------------------------------------------------------|
| `command`       | The command or script to execute and retry.                               |
| `max_retries`   | Maximum number of retries (e.g., `3` means 1 initial attempt + 3 retries). |
| `delay_seconds` | Delay in seconds between retries.                                         |

### Outputs

| Name      | Description                                                    |
|-----------|----------------------------------------------------------------|
| `outcome` | The final outcome of the command: `"success"` or `"failure"`. |

## Development and Testing

The action is implemented as a composite action using a bash script for the retry logic.

### Running Tests

Tests are defined as GitHub Actions workflows in the `tests/` directory. These workflows use the action with specially crafted commands that deterministically succeed or fail after a certain number of attempts.

To run the tests:

1.  Push your changes to a branch.
2.  Observe the `Test Flaky Command Forgiver` workflow run in your repository's Actions tab.

The tests are designed to be deterministic and offline:
-   **Mock rationale**: The `command` input for tests uses a simple file-based counter (`.retry_counter`) to simulate a command that fails a specific number of times before succeeding, or one that always fails. This ensures the tests do not rely on external services or network conditions, making them reliable and fast.
-   The `sleep` command for `delay_seconds` is a standard shell utility and its duration is controlled, ensuring deterministic delays.
