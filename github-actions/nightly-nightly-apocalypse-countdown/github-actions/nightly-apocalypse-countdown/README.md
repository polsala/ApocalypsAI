# nightly-apocalypse-countdown

A tiny GitHub Action that calculates the number of days remaining until a user‑specified "apocalypse" date and prints a whimsical message.  It can be used in any workflow to add a bit of fun to your CI runs.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `target_date` | The date of the apocalypse in `YYYY-MM-DD` format. | Yes | – |
| `current_date` | (Optional) Override the current date for deterministic runs, also `YYYY-MM-DD`. Useful for testing. | No | – |

## Outputs

The action simply echoes a message to the workflow log; it does not set any action outputs.

## Example usage

```yaml
name: Apocalypse Countdown
on: [push]

jobs:
  countdown:
    runs-on: ubuntu-latest
    steps:
      - name: Countdown to the end of the world
        uses: ./github-actions/nightly-apocalypse-countdown
        with:
          target_date: "2099-01-01"
```

## Testing

Run the provided test script locally:

```bash
cd github-actions/nightly-apocalypse-countdown
bash tests/test_countdown.sh
```

The test sets a mock current date and expects the correct output.
