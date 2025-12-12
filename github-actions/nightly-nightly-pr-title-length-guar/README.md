# PR Title Length Guard

A tiny, whimsical‑yet‑useful GitHub Action that ensures every pull‑request title stays within a sane length (default **72** characters).  If the title exceeds the limit the action fails the workflow and prints a friendly warning.

## Features

- Configurable `max-length` input (default: 72)
- Works as a **composite** action – no Docker image needed
- Pure Python implementation (runs on the default `ubuntu‑latest` runner)
- Fully unit‑tested (offline, deterministic)

## Usage

Add the following step to any workflow that runs on `pull_request` events:

```yaml
name: PR Title Lint
on: [pull_request]

jobs:
  title-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check PR title length
        uses: ./\.github/actions/pr-title-length-guard
        with:
          max-length: 80   # optional, overrides default of 72
```

The action will automatically read the PR title from the event payload supplied by GitHub and fail the job if the title is longer than the configured limit.

## Implementation Details

- The action is defined in `action.yml` as a **composite** action.
- The heavy lifting is done by `check_title.py`, a tiny Python script that reads the `GITHUB_EVENT_PATH` environment variable, parses the JSON payload, and compares the title length.
- The script exits with status `1` on failure, causing the step (and thus the job) to fail.

## Testing

Run the tests locally with:

```bash
python -m unittest discover -s tests
```

All tests are deterministic and use temporary JSON fixtures; no network access is required.
