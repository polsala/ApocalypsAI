# nightly-pr-whimsical-compliment

A tiny GitHub Action that selects a random whimsical compliment and posts it as a comment on a pull request. Perfect for adding a splash of positivity to code reviews.

## Features

- **Randomized compliments** from a curated list of quirky, uplifting phrases.
- **Zero external dependencies** – pure Python standard library.
- **Works as a reusable workflow** or a step in any workflow that has `pull_request` permissions.

## Usage

Add the following step to your workflow (e.g., `.github/workflows/ci.yml`):

```yaml
name: CI
on:
  pull_request:
    types: [opened, reopened]

jobs:
  compliment:
    runs-on: ubuntu-latest
    steps:
      - name: Add whimsical compliment
        uses: ./github-actions/nightly-pr-whimsical-compliment
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

The action expects a `github-token` input with permission to create comments on the PR.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token used to authenticate with the GitHub API. | Yes | N/A |

## Outputs

| Name | Description |
|------|-------------|
| `compliment` | The compliment that was posted. |

## How it works

The action runs a small Python script (`src/compliment.py`). The script:

1. Picks a random compliment from an internal list.
2. Calls the GitHub REST API to create a comment on the PR that triggered the workflow.
3. Exposes the selected compliment as an output (`compliment`).

## Testing

Unit tests are provided under `tests/`. They mock the GitHub API and verify that the script selects a valid compliment and formats the API request correctly.

## License

MIT © ApocalypsAI
