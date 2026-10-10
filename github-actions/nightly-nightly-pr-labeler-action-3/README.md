# PR Title Labeler Action

A tiny, whimsical GitHub Action that scans the title of a pull request and automatically adds one or more labels based on configurable keyword‑to‑label mappings.

## Features
- **Keyword‑driven**: Define any keyword → label mapping via a JSON input.
- **Zero‑runtime dependencies**: Pure Bash + `jq`; works on the default GitHub Actions runner.
- **Mock‑friendly**: If the `gh` CLI is not present (e.g., during offline tests) the action simply echoes the intended API call.

## Inputs
| Name | Description | Default |
|------|-------------|---------|
| `label-mapping` | JSON object where each key is a regex keyword and each value is the label to apply. | `{ "bug": "bug", "feature": "enhancement", "docs": "documentation" }` |

## Example Workflow
```yaml
name: PR Labeler
on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./
        with:
          label-mapping: '{"bug":"bug","feature":"enhancement","docs":"documentation"}'
```

## How It Works
1. The action reads the PR title from the event payload (`GITHUB_EVENT_PATH`).
2. It iterates over the provided mapping; if a keyword regex matches the title, the corresponding label is collected.
3. If the `gh` CLI is available, it calls the GitHub REST API to attach the labels. Otherwise it prints a mock message (useful for offline testing).

## Testing
The repository includes a Bash test (`tests/test_labeler.sh`) that runs the script with a fabricated event payload and a mocked `gh` command, asserting that the expected label is emitted.
