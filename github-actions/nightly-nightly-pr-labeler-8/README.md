# Nightly PR Labeler Action

## Overview

`nightly-pr-labeler` is a tiny composite GitHub Action that adds a label of your choice to the pull request that triggered the workflow. It is useful for automatically categorising PRs (e.g., `needs-review`, `automated`, `documentation`).

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `github-token` | A GitHub token with `repo` scope (usually `secrets.GITHUB_TOKEN`). | Yes |
| `label` | The label to add to the PR. | Yes |

## How it works

The action runs a small Bash script that reads the event payload (`GITHUB_EVENT_PATH`), extracts the PR number, and calls the GitHub REST API to add the label.

## Usage Example

```yaml
name: Add PR label
on:
  pull_request:
    types: [opened, reopened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - name: Label PR
        uses: ./utils/github-actions/nightly-pr-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          label: "automated"
```

## Testing

The utility includes a Bash test that mocks `curl` to verify the correct API request is made without contacting the real GitHub API. Run the test with:

```bash
bash tests/test_label_pr.sh
```

## License

MIT © ApocalypsAI
