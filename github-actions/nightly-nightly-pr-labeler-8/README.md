# Nightly PR Labeler

Automatically adds labels to pull requests based on title keywords.

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
      - uses: ./
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## How it works

The action looks at the PR title and adds one or more of the following labels:

- `bug` – if title contains "bug", "fix", "error"
- `feature` – if title contains "feat", "feature", "add"
- `docs` – if title contains "doc", "readme", "docs"
- `chore` – if none of the above, adds `chore`

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `github_token` | Token with repo scope to call the API | true |

## License

MIT
