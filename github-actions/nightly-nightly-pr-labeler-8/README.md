# Nightly PR Labeler

Utility that automatically adds appropriate labels to a pull request based on keywords in its title. Supports `[bug]` → `bug`, `[feature]` → `enhancement`. Can be used as a reusable GitHub Action.

## Usage

```yaml
jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Label PR
        uses: ./utils/nightly-pr-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
```

## Inputs

- `github-token` – token with repo scope (required).

## Outputs

- `labels` – comma‑separated list of labels added.
