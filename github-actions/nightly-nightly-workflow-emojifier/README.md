# Nightly Workflow Emojifier

A GitHub Action that adds a touch of whimsy to your CI/CD by translating workflow job statuses into delightful emojis. Perfect for adding a visual flourish to PR comments, status badges, or custom notifications!

## Usage

Add this action to your workflow to get an emoji based on a job's status.

```yaml
name: Whimsical Status Example

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Simulate a successful build
        run: echo "Build successful!"

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Simulate a failing test
        run: exit 1 # This job will fail

  emojify_status:
    runs-on: ubuntu-latest
    needs: [build, test] # Depends on both build and test jobs
    steps:
      - name: Get Build Job Emoji
        id: build_emoji
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-emojifier@main # Replace with actual path
        with:
          status: ${{ needs.build.result }}
          default-emoji: '❓'

      - name: Get Test Job Emoji
        id: test_emoji
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-emojifier@main # Replace with actual path
        with:
          status: ${{ needs.test.result }}
          default-emoji: '🤷'

      - name: Get Overall Workflow Status Emoji
        id: workflow_emoji
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-emojifier@main # Replace with actual path
        with:
          status: ${{ job.status }} # This job's status (will be success if previous steps pass)
          default-emoji: '🤔'

      - name: Print Emojis
        run: |
          echo "Build Status: ${{ steps.build_emoji.outputs.emoji }}"
          echo "Test Status: ${{ steps.test_emoji.outputs.emoji }}"
          echo "Overall Emojifier Job Status: ${{ steps.workflow_emoji.outputs.emoji }}"

      - name: Add a whimsical comment to PR (example)
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `✨ Workflow Update ✨\n\nBuild: ${{ steps.build_emoji.outputs.emoji }}\nTests: ${{ steps.test_emoji.outputs.emoji }}\n\nKeep up the great work!`
            })
```

## Inputs

| Name            | Description                                     | Required | Default |
| :-------------- | :---------------------------------------------- | :------- | :------ |
| `status`        | The status string (e.g., `success`, `failure`, `cancelled`, `skipped`). | `true`   |         |
| `default-emoji` | The emoji to use if the status is not recognized. | `false`  | `❓`    |

## Outputs

| Name     | Description                  |
| :------- | :--------------------------- |
| `emoji`  | The whimsical emoji for the status. |

## Development

To run tests locally:
```bash
npm install
npm test
```
