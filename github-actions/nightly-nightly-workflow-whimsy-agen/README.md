# Nightly Workflow Whimsy Agent

A GitHub Action that injects a dose of whimsy and morale into your workflow runs by posting delightful comments on associated Pull Requests. Whether your workflow succeeds, fails, or is cancelled, the Whimsy Agent has a cosmic message for you!

## 🌌 How it Works

This action listens for `workflow_run` events. When a workflow completes, it checks the conclusion (success, failure, or cancelled) and generates a unique, whimsical message. If the workflow is associated with a Pull Request, the agent will post this message as a comment on that PR, offering encouragement, celebration, or philosophical reflection.

## ✨ Usage

To use the Nightly Workflow Whimsy Agent, add it to one of your existing workflows that you want to monitor, or create a new one.

### Example Workflow (`.github/workflows/whimsy-monitor.yml`)

```yaml
name: Whimsy Workflow Monitor

on:
  workflow_run:
    workflows: ["Your CI Workflow Name Here"] # Replace with the name of the workflow you want to monitor
    types:
      - completed

jobs:
  whimsy_comment:
    runs-on: ubuntu-latest
    steps:
      - name: Extract PR Number
        id: get_pr_number
        run: |
          PR_NUMBER=""
          if [ "${{ github.event.workflow_run.pull_requests }}" != "[]" ]; then
            PR_NUMBER=$(echo '${{ github.event.workflow_run.pull_requests[0].number }}')
          fi
          echo "pr_number=$PR_NUMBER" >> $GITHUB_OUTPUT
        shell: bash

      - name: Post Whimsical Comment
        uses: polsala/ApocalypsAI/nightly-workflow-whimsy-agent@main # Adjust path if this is a sub-directory
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          workflow-conclusion: ${{ github.event.workflow_run.conclusion }}
          pr-number: ${{ steps.get_pr_number.outputs.pr_number }}
```

**Note:**
- Replace `"Your CI Workflow Name Here"` with the actual `name` field of the workflow you wish to monitor.
- The `github-token` requires `pull-requests: write` permission for the workflow that *uses* this action to post comments. Ensure your workflow has this permission:
  ```yaml
  permissions:
    pull-requests: write
    issues: write # Issues write is also needed for comments
  ```

## 🚀 Inputs

| Input Name          | Description                                                              | Required |
|---------------------|--------------------------------------------------------------------------|----------|
| `github-token`      | GitHub token for posting comments. Usually `${{ secrets.GITHUB_TOKEN }}`. | Yes      |
| `workflow-conclusion` | The conclusion of the workflow run (e.g., `success`, `failure`, `cancelled`). | Yes      |
| `pr-number`         | The pull request number to comment on, if applicable.                    | No       |

## 📦 Outputs

| Output Name       | Description                                  |
|-------------------|----------------------------------------------|
| `whimsical-message` | The generated whimsical message.             |
| `comment-id`      | The ID of the created comment, if any.       |

## 🧪 Development & Testing

This action includes unit tests for its core logic using Jest.

To run tests locally:
1. Navigate to the `nightly-workflow-whimsy-agent` directory.
2. Install dependencies: `npm install`
3. Run tests: `npm test`

The tests mock GitHub API interactions to ensure deterministic and offline execution.
