# Nightly Victory Toast Action

This GitHub Action celebrates successful workflow runs by posting a whimsical victory toast message as a comment on a GitHub Pull Request or Issue.

## Usage

Add this action to your workflow, typically after all other steps have completed successfully.

```yaml
name: My Awesome Workflow
on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run some tests
        run: echo "Tests passed!"

      - name: Post Victory Toast
        if: success()
        uses: polsala/ApocalypsAI/nightly-victory-toast-action@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: Specify a target PR/Issue number if not triggered by a PR event
          # target-pr-number: ${{ github.event.pull_request.number }}
          # target-issue-number: 123
          # Optional: Custom message
          # message: "Our code stands strong against the void!"
```

### Inputs

*   `github-token`: **(Required)** A GitHub token with `issues:write` permission. Typically `${{ secrets.GITHUB_TOKEN }}`.
*   `message`: (Optional) A custom victory message. If not provided, a random whimsical message will be chosen.
*   `target-pr-number`: (Optional) The number of the Pull Request to comment on. If provided, this takes precedence over `github.event.pull_request.number`.
*   `target-issue-number`: (Optional) The number of the Issue to comment on. If provided, this takes precedence over `target-pr-number` and `github.event.pull_request.number`.

### Outputs

*   `comment-url`: The URL of the created comment, if a comment was successfully posted.

## How it works

1.  Retrieves the `github-token` and optional `message`, `target-pr-number`, `target-issue-number` inputs.
2.  Determines the target for the comment:
    *   If `target-issue-number` is provided, it comments on that issue.
    *   Else if `target-pr-number` is provided, it comments on that PR.
    *   Else if the workflow was triggered by a `pull_request` event, it comments on that PR.
    *   Else if the workflow was triggered by an `issue` event, it comments on that issue.
    *   Otherwise, it logs the message to the workflow output without posting a comment.
3.  If a target is found, it constructs a whimsical message (or uses the custom one) and posts it as a comment.
4.  Sets the `comment-url` output if a comment was created.
