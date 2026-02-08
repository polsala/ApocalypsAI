# Nightly PR Keyword Labeler

A GitHub Action that automatically adds whimsical labels to pull requests based on keywords found in the PR title. Perfect for adding fun flair to your repo without manual effort.

## Inputs

- `github-token` (required): Token with `contents: read` and `pull-requests: write` scopes.
- `label-mapping` (optional): JSON string mapping keywords to labels. Default mapping includes:
  ```json
  {
    "fix": "🛠️ bugfix",
    "feature": "✨ feature",
    "docs": "📚 documentation",
    "refactor": "♻️ refactor",
    "wip": "🚧 WIP"
  }
  ```

## How it works

The action runs on `pull_request_target` events (`opened`, `edited`, `reopened`). It fetches the PR title, checks for any of the configured keywords (case‑insensitive), and adds the corresponding label(s) via the GitHub API.

## Example workflow

```yaml
name: PR Keyword Labeller
on:
  pull_request_target:
    types: [opened, edited, reopened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: ./.github/actions/nightly-pr-keyword-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## License

MIT
