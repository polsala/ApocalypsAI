# Nightly Issue Fortune Teller

A GitHub Action that posts a whimsical fortune comment on newly opened issues. It extracts keywords from the issue title and generates a playful fortune.

## Usage

```yaml
name: Issue Fortune
on:
  issues:
    types: [opened]

jobs:
  fortune:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Post Fortune
        uses: ./github-actions/nightly-issue-fortune-teller
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `github-token` (required): Token with repo scope to post comments.

## How it works

The action runs a small Bash script that:

1. Reads the issue title from the `GITHUB_EVENT_PATH` JSON file.
2. Picks a random fortune template.
3. Inserts any detected keyword (e.g., "bug", "feature") into the template.
4. Posts the comment via the GitHub REST API.

## License

MIT
