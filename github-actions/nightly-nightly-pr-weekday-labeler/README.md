# Nightly PR Weekday Labeler

This GitHub Action determines the weekday (e.g., Monday) for a given date or for the current day and exposes it as an output `weekday`. It can be used to automatically add weekday‑based labels to pull requests or to drive conditional workflow logic.

## Inputs

- `date` (optional): An ISO‑format date string (`YYYY‑MM‑DD`). If omitted, the action uses the current UTC date.

## Outputs

- `weekday`: The name of the weekday (`Monday`, `Tuesday`, …).

## Usage

```yaml
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: ./nightly-pr-weekday-labeler
        id: weekday
        with:
          date: '2023-10-31'   # optional
      - name: Add label
        if: steps.weekday.outputs.weekday == 'Tuesday'
        run: |
          gh pr edit ${{ github.event.pull_request.number }} --add-label "Tuesday"
```

## Implementation Details

The action is a **composite** action that runs a small Bash script (`src/determine_weekday.sh`). The script reads the optional `date` input, computes the weekday using GNU `date`, and writes the result to `$GITHUB_OUTPUT`.

## Testing

Run the test script locally:

```bash
bash tests/test_determine_weekday.sh
```

It should output `PASS`.
