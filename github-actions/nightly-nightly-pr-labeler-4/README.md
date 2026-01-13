# Nightly PR Labeler

A tiny GitHub Action that scans the title of a pull request and adds one or more labels based on a userâprovided keywordâtoâlabel map.

## Features

- **Zeroâruntime dependencies** â pure Node.js (no external packages).
- **Configurable mapping** â supply a JSON object where keys are keywords (caseâinsensitive) and values are the labels to apply.
- **Safe defaults** â if no keyword matches, the action does nothing.

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | A token with `pull_request` write permissions (usually `{{ secrets.GITHUB_TOKEN }}`). | true | â |
| `label-mapping` | JSON string mapping keywords to label names. Example: `{ "bug": "bug", "feat": "feature" }`. | true | â |

## Example workflow

```yaml
name: Autoâlabel PRs

on:
  pull_request:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntuâlatest
    steps:
      - uses: actions/checkout@v3
      - name: Apply labels
        uses: ./github-actions/nightly-pr-labeler
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          label-mapping: '{"bug":"bug","feat":"feature","doc":"documentation"}'
```

## How it works

1. The action reads the event payload from `GITHUB_EVENT_PATH` (provided by GitHub).
2. It extracts the PR title.
3. It iterates over the supplied mapping; for each keyword that appears in the title (caseâinsensitive) the corresponding label is collected.
4. If any labels are found, the action calls the GitHub REST API `POST /repos/{owner}/{repo}/issues/{issue_number}/labels` to apply them.

## Development & Testing

The core labelâmatching logic lives in `src/index.js` and is unitâtested in `tests/test_index.js`. Run the tests locally with:

```bash
node tests/test_index.js
```

## License

MIT
