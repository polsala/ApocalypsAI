# Nightly PR Labeler

Utility: A GitHub Action that automatically adds labels to pull requests based on keywords in the PR title.

## Usage

```yaml
uses: polsala/ApocalypsAI/github-actions/nightly-pr-labeler@v1
with:
  mapping: |
    bug:bug
    feat:enhancement
    docs:documentation
```

The action reads the PR title and adds the corresponding label if a keyword matches.

## How it works

- Reads `GITHUB_EVENT_PATH` JSON file to get `pull_request.title`.
- For each `keyword:label` pair in `mapping`, checks if title contains keyword (case‑insensitive).
- Emits `::add-label::<label>` command for GitHub to apply.

## Limitations

- Only works on pull request events.
- First matching keyword wins.
