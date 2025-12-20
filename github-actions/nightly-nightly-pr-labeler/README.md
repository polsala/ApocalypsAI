# Nightly PR Labeler

Automatically adds whimsical labels to pull requests based on title keywords.

## Usage

Create a workflow that uses this action on `pull_request_target` events.

```yaml
name: PR Labeler
on:
  pull_request_target:
    types: [opened, edited, reopened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./utils/nightly-pr-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

The action looks for keywords in the PR title and adds the corresponding label:

- `urgent` → 🌟 `high priority`
- `wip` → 🛠️ `work in progress`
- `fix` → 🐞 `bug fix`
- `feature` → ✨ `new feature`
- `zombie` → 🧟 `zombie PR` (stale or forgotten)

If no keyword matches, no label is added.

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `github-token` | Token with repo scope to add labels | Yes |

## License

MIT
