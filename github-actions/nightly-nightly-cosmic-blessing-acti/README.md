# Nightly Cosmic Blessing Action

## Overview

The `nightly-cosmic-blessing-action` is a whimsical GitHub Action designed to bring a touch of interdimensional joy to your development workflow. Upon successful completion of a workflow, this action will post a random, positive, and slightly absurd "cosmic blessing" as a comment on the associated Pull Request or Issue. It's a fun way to celebrate successes and boost team morale!

## Features

*   **Whimsical Blessings**: Choose from a set of default cosmic messages or provide your own.
*   **Automated Morale Boost**: Automatically congratulates your team on successful merges or deployments.
*   **Easy Integration**: Simple to add to any existing GitHub Actions workflow.

## Usage

To use this action, add it as a step in your GitHub Actions workflow. It typically runs after your main build, test, or deployment steps have successfully completed.

### Example Workflow (`.github/workflows/bless-on-success.yml`)

```yaml
name: Cosmic Blessing on PR Merge

on: pull_request

jobs:
  build_and_test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests (replace with your actual build/test steps)
        run: echo "Simulating successful build and tests..."

  post_blessing:
    needs: build_and_test # Ensure blessing only runs after success
    if: success() && github.event_name == 'pull_request' && github.event.action == 'closed' && github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Post Cosmic Blessing
        uses: polsala/ApocalypsAI/.github/actions/nightly-cosmic-blessing-action@main # Adjust path if this action is moved
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: Provide custom blessings (comma-separated)
          # blessings: 'You are a star!, The universe smiles upon your code!, Your commit is legendary!'
```

### Inputs

*   `token`: **(Required)** Your GitHub Token. Use `${{ secrets.GITHUB_TOKEN }}` for automatic authentication.
*   `blessings`: **(Optional)** A comma-separated string of custom blessing messages. If not provided, a default set of whimsical blessings will be used.

### Outputs

*   `blessing-message`: The specific blessing message that was posted to the PR/Issue.

## Development

This action is written in JavaScript and uses the GitHub Actions Toolkit.

### Running Tests

Tests are written with Jest. To run them locally:

1.  Navigate to the action's directory.
2.  Install dependencies: `npm install` (assuming `package.json` is present with `jest` and `@actions/core`, `@actions/github`)
3.  Run tests: `npm test`

## Contributing

Feel free to suggest new whimsical blessings or improvements! Open an issue or pull request in the main repository.
