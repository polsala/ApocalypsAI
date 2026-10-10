# Nightly Apocalypse Friday Labeler

## Overview

`nightly-apocalypse-friday-labeler` is a GitHub Action that adds a custom label (default: `post-apocalypse`) to any issue that is opened on a **Friday**.  It adds a touch of post‑apocalyptic flair to your repository while keeping track of weekend‑ready issues.

## Features

- Detects the day of the week from the issue creation timestamp.
- Adds a configurable label (default `post-apocalypse`).
- Works with both public and private repositories using a provided `GITHUB_TOKEN`.
- Implemented as a lightweight Docker‑based action (Alpine + Bash).

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token with `issues:write` permission (usually `${{ secrets.GITHUB_TOKEN }}`). | Yes | N/A |
| `label-name` | Name of the label to apply when the issue is opened on Friday. | No | `post-apocalypse` |

## Usage

Add the following step to your workflow (e.g., `.github/workflows/issue-friday-label.yml`):

```yaml
name: Friday Issue Labeler
on:
  issues:
    types: [opened]

jobs:
  label-friday:
    runs-on: ubuntu-latest
    steps:
      - name: Apply Friday Apocalypse Label
        uses: ./github-actions/nightly-apocalypse-friday-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # label-name: "post-apocalypse"  # optional custom label
```

## How It Works

1. GitHub passes the event payload to the action via the `GITHUB_EVENT_PATH` environment variable.
2. The Bash entrypoint parses the `created_at` timestamp.
3. If the day of week is Friday, it sends a `POST /issues/{issue_number}/labels` request using `curl`.

## Testing

Run the provided test script locally:

```bash
cd github-actions/nightly-apocalypse-friday-labeler
bash tests/test_entrypoint.sh
```

The test uses a mocked `curl` function to verify that the correct API call would be made without contacting the real GitHub API.

## License

MIT © ApocalypsAI
