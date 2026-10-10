# nightly‑issue‑fortune

A tiny GitHub Action that adds a random, whimsical fortune‑cookie style comment to every newly opened issue.  It’s a fun way to greet contributors and sprinkle a little mystery into your repository.

## Features

- Picks a random fortune from a curated list of 20+ quirky sayings.
- Runs automatically on the `issues` event when an issue is **opened**.
- Uses the provided `GITHUB_TOKEN` to post the comment, so no extra permissions are required.
- Fully self‑contained – no external API calls, works offline.

## Usage

Add the following step to your workflow (or copy the example workflow below).

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
      - name: Post a fortune comment
        uses: ./github-actions/nightly-issue-fortune
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token with permission to create issue comments (usually `secrets.GITHUB_TOKEN`). | Yes | N/A |

## Development

The action is written in JavaScript (Node.js) and uses the official `@actions/core` and `@actions/github` packages.

### Running tests locally

```bash
# Install dependencies
npm install
# Run the test suite
npm test
```

## License

MIT © ApocalypsAI
