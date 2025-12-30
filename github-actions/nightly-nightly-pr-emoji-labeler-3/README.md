# PR Emoji Labeler

A GitHub Action that scans the pull request title for specific emojis and automatically adds corresponding labels.

## How it works

- 🚀 → `enhancement`
- 🐛 → `bug`
- 📚 → `documentation`

Add any of these emojis to your PR title and the action will label the PR accordingly.

## Usage

```yaml
name: PR Emoji Labeler
on:
  pull_request:
    types: [opened, edited, reopened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./path/to/nightly-pr-emoji-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token with repo scope to add labels | true | N/A |

## License

MIT
