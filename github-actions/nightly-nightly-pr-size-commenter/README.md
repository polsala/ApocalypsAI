# Nightly PR Size Commenter

A whimsical GitHub Action that evaluates the size of a pull request (based on the total number of added and removed lines) and leaves a friendly comment on the PR describing its magnitude.

## Features

- Categorises PR size into **Tiny**, **Small**, **Medium**, or **Large**.
- Adds a fun emoji and a short description as a comment on the PR.
- Exposes the size category as an output for downstream steps.

## Usage

Add the action to your workflow (e.g., `.github/workflows/pr-size-comment.yml`):

```yaml
name: PR Size Commenter
on:
  pull_request_target:
    types: [opened, synchronize]

jobs:
  comment-size:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Comment PR size
        uses: ./nightly-pr-size-commenter
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `github-token` | A token with `repo` scope (usually `secrets.GITHUB_TOKEN`). | Yes |

## Outputs

| Name | Description |
|------|-------------|
| `size-category` | One of `tiny`, `small`, `medium`, `large`. |

## Development

The action is written in JavaScript and uses the official `@actions/github` and `@actions/core` packages.

Run tests locally with:

```bash
npm install
npm test
```

## License

MIT © ApocalypsAI
