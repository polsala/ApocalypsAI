# nightly-pr-labeler

A tiny GitHub Action that inspects the pull request title and automatically adds appropriate labels. It looks for common keywords like `bug`, `feature`, `docs`, and also tacks on a random whimsical emoji label for extra flair.

## Usage

Create a workflow that runs on `pull_request_target` (or `pull_request`) and uses this action:

```yaml
name: Auto‑label PRs
on:
  pull_request:
    types: [opened, edited, reopened]

jobs:
  label:
    runs-on: ubuntu‑latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./github-actions/nightly-pr-labeler
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The action will add the computed labels via the GitHub API.

## How it works

1. Reads the PR event payload from `$GITHUB_EVENT_PATH`.
2. Determines labels:
   * `bug` → if title contains “bug” (case‑insensitive)
   * `feature` → if title contains “add”, “implement”, “feature”
   * `docs` → if title contains “doc”, “readme”, “documentation”
   * `emoji‑<emoji>` → a random emoji from a predefined list.
3. Calls the GitHub REST API to add the labels.

## Testing

Run the test script locally:

```sh
bash tests/test_labeler.sh
```

It uses mocked event data and a mock `curl` to verify the correct labels are sent.
