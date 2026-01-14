# Nightly PR Labeler

A tiny GitHub Action that automatically adds labels to pull requests based on the PR title and a random emoji label for a touch of whimsy.

## Features

- Detects common conventional‑commit prefixes (`feat`, `fix`, `docs`, `chore`, `refactor`, `test`) and adds a corresponding label (`feature`, `bug`, `documentation`, `chore`, `refactor`, `tests`).
- Optionally picks a random emoji label from a user‑provided list (default: `✨,🚀,🧪,🐛`).
- Works on `pull_request` events (`opened`, `reopened`, `synchronize`).

## Usage

Create a workflow file (e.g. `.github/workflows/pr-labeler.yml`):

```yaml
name: PR Labeler
on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Nightly PR Labeler
        uses: ./nightly-pr-labeler
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: custom emoji list (comma‑separated)
          # emoji_labels: "🌟,🔥,💡"
```

> **Note**: The action expects the repository checkout to be present because it runs as a local action (`uses: ./nightly-pr-labeler`). If you publish the action to the marketplace, replace the path with `owner/repo@v1`.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github_token` | GitHub token with `repo` scope (usually `${{ secrets.GITHUB_TOKEN }}`). | Yes | `${{ github.token }}` |
| `emoji_labels` | Comma‑separated list of emoji labels to choose from. | No | `✨,🚀,🧪,🐛` |

## Development

```bash
# Install dependencies
npm install

# Run tests
npm test
```

## License

MIT © ApocalypsAI
