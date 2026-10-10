# nightly-pr-labeler

A GitHub Action that automatically adds labels to a pull request based on the files changed. It also adds a random emoji as an extra label for a touch of fun.

## Inputs

- `github-token` (required): Token with repo scope.
- `label-mapping` (optional): JSON string mapping glob patterns to label names. Example: `{"*.md":"documentation","src/**/*.py":"python"}`

## How it works

1. Lists files changed in the PR.
2. Matches each file against the provided glob patterns.
3. Adds the corresponding labels.
4. Picks a random emoji from a built‑in list and adds it as an additional label.

## Example workflow

```yaml
name: Auto‑label PRs
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu‑latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./nightly-pr-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          label-mapping: '{"*.md":"documentation","src/**/*.py":"python"}'
```

## License

MIT
