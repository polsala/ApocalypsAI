# Nightly PR Quote Commenter

A tiny GitHub Action that automatically leaves a whimsical quote as a comment on every newly opened pull request. Perfect for adding a splash of inspiration (or pure silliness) to your PR workflow.

## Features
- Deterministic quote selection based on the PR number, so the same PR always gets the same quote.
- No external dependencies beyond the standard GitHub Actions environment (uses `bash`, `curl`, and `jq`).
- Fully testable offline with a mock `curl` command.

## Usage
Create a workflow in your repository (e.g. `.github/workflows/pr-quote.yml`):

```yaml
name: PR Quote Commenter
on:
  pull_request:
    types: [opened]

jobs:
  add-quote:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Post a whimsical quote
        uses: ./github-actions/nightly-pr-quote-commenter
        with:
          # No inputs required
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The action will read the pull request number from the event payload, pick a quote, and post it as a comment.

## How it works
1. The action reads `GITHUB_EVENT_PATH` to obtain the PR number.
2. It selects a quote from a hard‑coded list using `PR_NUMBER % number_of_quotes`.
3. It posts the comment via the GitHub REST API using `curl`.

## Testing
Run the provided test script locally:

```bash
cd github-actions/nightly-pr-quote-commenter/tests
bash test_action.sh
```
The test mocks the GitHub environment and verifies that the expected quote is sent to the mocked `curl` command.

## License
MIT © ApocalypsAI
