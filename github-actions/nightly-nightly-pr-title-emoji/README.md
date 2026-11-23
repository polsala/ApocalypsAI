# nightly-pr-title-emoji

A whimsical GitHub Action that appends a random emoji to the title of a pull request when the workflow runs. Perfect for adding a touch of personality to your PR list.

## Usage

```yaml
name: PR Emoji Enhancer
on:
  pull_request:
    types: [opened, edited, reopened]

jobs:
  add-emoji:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Append Emoji to PR Title
        uses: ./ # if using local action, otherwise use a repo reference
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token with repo scope to edit PR titles. | true | N/A |

## Outputs

| Name | Description |
|------|-------------|
| `emoji` | The emoji that was appended. |

## How it works

The action picks a random emoji from a curated list and updates the PR title via the GitHub REST API.

## Testing

Run `npm test` to execute the Jest test suite, which mocks the GitHub API.
