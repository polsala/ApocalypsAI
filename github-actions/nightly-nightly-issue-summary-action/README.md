# Issue Summary Action

Generates a markdown summary of all open issues in the repository, grouped by label, and posts it as a comment on the pull request.

## Usage

```yaml
name: Issue Summary
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  summarize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate issue summary
        uses: ./ # uses the action in this repository
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `github_token` (required): Token with repo scope to query issues and post comment.

## Output

The action posts a comment on the PR with the generated markdown.

## Implementation

The action runs a small Bash script that calls the GitHub REST API and formats the result.
