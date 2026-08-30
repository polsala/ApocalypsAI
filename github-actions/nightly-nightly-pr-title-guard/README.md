# PR Title Guard Action

## Overview

`nightly-pr-title-guard` is a reusable GitHub Action that validates the title of a pull request against a required prefix (e.g., `feat:`, `fix:`). If the title does not start with the configured prefix, the action fails, causing the workflow to stop.

## Why?

Consistent PR titles make changelogs, release notes, and automation easier to generate. This tiny guard helps teams enforce a naming convention without writing custom scripts.

## Inputs

| Name   | Description                                 | Required | Default |
|--------|---------------------------------------------|----------|---------|
| `prefix` | The required prefix for the PR title (e.g., `feat:`). | Yes      | N/A     |

## Usage

Add the action to any workflow that runs on `pull_request` events:

```yaml
name: PR Title Check
on:
  pull_request:
    types: [opened, edited, synchronize]

jobs:
  title-check:
    runs-on: ubuntu-latest
    steps:
      - name: Check PR title prefix
        uses: ./nightly-pr-title-guard
        with:
          prefix: "feat:"
```

The action will read the `GITHUB_EVENT_PATH` environment variable (automatically provided by GitHub) to obtain the PR title.

## Testing

The `tests/` directory contains a Bash test script that runs the underlying Python validator with mocked event payloads. Run it locally with:

```bash
cd nightly-pr-title-guard/tests
bash test_check_pr_title.sh
```

All tests should pass.

## License

MIT © ApocalypsAI
