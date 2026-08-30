# Nightly Workflow Emote Generator

A whimsical GitHub Action that generates a cosmic emoji or message based on the status of a previous workflow step or job. Inject some personality into your CI/CD notifications!

## ✨ Features

*   **Status-based Emotes**: Provides unique, whimsical messages for `success`, `failure`, `cancelled`, and `skipped` statuses.
*   **Easy Integration**: Simple to add to any GitHub Actions workflow.

## 🚀 Usage

Add this action to your workflow to generate an emote based on a previous step's outcome. You can then use this emote in subsequent steps, for example, to post a comment, update a status check, or send a notification.

### Example Workflow

```yaml
name: Cosmic Build & Emote

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Simulate a build step (can be success or failure)
        id: build_step
        run: |
          # Simulate success for demonstration
          echo "Build successful!"
          # To simulate failure, uncomment the line below:
          # exit 1

      - name: Generate Emote for Build Status
        id: emote_gen
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-emote-gen@main # Adjust path if needed
        with:
          status: ${{ steps.build_step.outcome }} # Use 'outcome' for step status, or 'result' for job status

      - name: Display the Emote
        run: |
          echo "Workflow Status Emote: ${{ steps.emote_gen.outputs.emote }}"

      - name: Post Emote as a PR Comment (Example)
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `The build step concluded with: **${{ steps.emote_gen.outputs.emote }}**`
            })
```

### Inputs

| Name     | Description                                                              | Required |
| :------- | :----------------------------------------------------------------------- | :------- |
| `status` | The status of the previous workflow step or job (e.g., `success`, `failure`, `cancelled`, `skipped`). | `true`   |

### Outputs

| Name    | Description                                                     |
| :------ | :-------------------------------------------------------------- |
| `emote` | A whimsical emoji or message representing the workflow status. |

## 🛠️ Development

### Testing

The action's core logic can be tested locally using the provided bash test script:

```bash
bash tests/test_generate_emote.sh
```

This script simulates the GitHub Actions environment variables and output mechanism to ensure the correct emotes are generated for various statuses.
