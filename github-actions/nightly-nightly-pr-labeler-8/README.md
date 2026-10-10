# PR Labeler Action

Automatically adds labels to pull requests based on keywords in the PR title.

## Usage

```yaml
name: Auto label PRs
on:
  pull_request:
    types: [opened, edited, reopened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./  # assuming the action is in the repository root
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```

The action looks for the following keywords (case‑insensitive):

- `fix`, `bug` → **bug**
- `feat`, `feature` → **enhancement**
- `doc`, `docs` → **documentation**

Multiple labels can be applied if multiple keywords are present.

## Development

Run tests with:

```sh
npm install
npm test
```
