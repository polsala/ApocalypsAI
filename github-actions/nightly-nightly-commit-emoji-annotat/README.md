# Commit Emoji Annotator

A whimsical GitHub Action that scans the commits of a pull request and adds an emoji reaction to each commit based on a very simple sentiment analysis of the commit message.

## How it works

1. The action receives a `GITHUB_TOKEN` (automatically provided by GitHub) and the pull request number.
2. It fetches the list of commits in the PR.
3. For each commit message it checks for positive words (`feat`, `add`, `improve`, `fix`) or negative words (`bug`, `remove`, `fail`, `break`).
4. It adds a reaction:
   * 👍 for positive
   * 👎 for negative
   * 🤔 for neutral / none of the above

## Usage

```yaml
name: Annotate Commits with Emojis
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  annotate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Commit Emoji Annotator
        uses: ./ # if the action lives in the same repo
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pull-number: ${{ github.event.pull_request.number }}
```

## Inputs

| Name | Description | Required |
|------|-------------|----------|
| `github-token` | Token with repo scope (usually `GITHUB_TOKEN`). | Yes |
| `pull-number` | Pull request number to annotate. | Yes |

## License

MIT
