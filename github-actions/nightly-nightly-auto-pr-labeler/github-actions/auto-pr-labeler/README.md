# Auto PR Labeler

A GitHub Action that automatically adds whimsical labels to pull requests based on keywords in the PR title.

## Usage

Create a workflow file:

```yaml
name: Auto PR Labeler
on:
  pull_request:
    types: [opened, edited, reopened]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./github-actions/auto-pr-labeler
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

The action looks for the following keywords (caseâinsensitive) and adds the corresponding labels:

- `fix` â ð§ zombieâfix
- `feature` â âï¸ sunriseâfeature
- `doc` â ð documentation
- `refactor` â ð§ refactor
- `test` â â testâaddition

If no keywords match, the action does nothing.

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `repo-token` | GitHub token with repo scope (usually `GITHUB_TOKEN`) | Yes |

## License

MIT
