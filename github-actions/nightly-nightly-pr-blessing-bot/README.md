# Nightly PR Blessing Bot

A GitHub Action that adds a whimsical, apocalypse-themed blessing comment to successfully merged Pull Requests. This encourages contributors and adds a unique, positive touch to the merge process.

## Features

*   **Whimsical Blessings**: Posts a random affirmation, emoji, or quote related to the ApocalypsAI theme.
*   **Configurable**: Choose the type of blessing to post.
*   **Automated**: Runs automatically on `pull_request` `closed` events when a PR is merged.

## Usage

To use this action, add a new step to your existing workflow (e.g., your CI/CD workflow that runs on `pull_request` events) or create a new workflow specifically for blessings.

### Example Workflow (`.github/workflows/bless-pr.yml`)

```yaml
name: PR Blessing

on:
  pull_request:
    types:
      - closed

jobs:
  bless:
    runs-on: ubuntu-latest
    if: github.event.pull_request.merged == true
    steps:
      - name: Post ApocalypsAI Blessing
        uses: ./github-actions/nightly-pr-blessing-bot@main # Path to this action within the repository
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          blessing-type: 'affirmation' # Optional: 'emoji', 'quote', or 'affirmation' (default)
```

### Inputs

*   `github-token` (required):
    A GitHub token with `pull-requests: write` permission. Typically `${{ secrets.GITHUB_TOKEN }}`.
*   `blessing-type` (optional, default: `affirmation`):
    The type of blessing to post. Can be `affirmation`, `emoji`, or `quote`.

## Development

This action is built with Node.js. To develop and test locally:

1.  **Install Dependencies**:
    ```bash
    npm install
    ```
2.  **Build the Action**:
    ```bash
    npm run build
    ```
    This compiles `src/index.js` into `dist/index.js` using `@vercel/ncc`.
3.  **Run Tests**:
    ```bash
    npm test
    ```
