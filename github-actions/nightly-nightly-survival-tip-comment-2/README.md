# Survival Tip Commenter Action

A whimsical GitHub Action that selects a post‑apocalyptic survival tip and makes it available as an output (`tip`). Optionally it can post the tip as a comment on a pull request.

## Usage

```yaml
name: Survival Tip

on:
  pull_request:
    types: [opened, reopened]

jobs:
  tip:
    runs-on: ubuntu-latest
    steps:
      - uses: ./ # uses the action in this repository
        id: tip
        with:
          token: ${{ secrets.GITHUB_TOKEN }} # optional, posts comment

      - name: Show tip
        run: echo "Tip: ${{ steps.tip.outputs.tip }}"
```

## Inputs

- `token` – (optional) GitHub token used to post a comment on the PR.

## Outputs

- `tip` – The selected survival tip.

The tip is chosen deterministically based on the workflow run number, so repeated runs produce predictable results (useful for testing).
