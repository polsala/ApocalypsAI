# Nightly Workflow Emojifier

Converts GitHub Actions workflow run statuses into whimsical emoji sequences for quick visual feedback in your CI/CD pipelines.

## ✨🚀🎉 What it does

This GitHub Action takes a workflow run status (e.g., `success`, `failure`, `cancelled`) and transforms it into a fun, memorable string of emojis. This can be used to enrich workflow summaries, PR comments, or any other place where a quick, visual status indicator is desired.

## 🛠️ How to use

Add this action to your workflow. It requires the `status` of a job or workflow run as an input.

```yaml
name: Example Workflow with Emojifier
on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Simulate a successful step
        run: echo "Build successful!"

  report_status:
    runs-on: ubuntu-latest
    needs: build
    if: always() # Ensure this job runs even if 'build' fails
    steps:
      - name: Get build job status
        id: get_status
        run: |
          echo "status=${{ needs.build.result }}" >> "$GITHUB_OUTPUT"

      - name: Emojify the status
        id: emojify_status
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-emojifier@main # Replace 'main' with your branch/tag
        with:
          status: ${{ steps.get_status.outputs.status }}

      - name: Output Emojis
        run: |
          echo "The build status emojis are: ${{ steps.emojify_status.outputs.emojis }}"
          # You can use this output in a PR comment, workflow summary, etc.
          # For example, to add to a workflow summary:
          echo "### Build Status: ${{ steps.emojify_status.outputs.emojis }}" >> "$GITHUB_STEP_SUMMARY"

```

## 🚀 Inputs

| Name   | Description                               | Type     | Required | Default |
| :----- | :---------------------------------------- | :------- | :------- | :------ |
| `status` | The status of the workflow run or job.    | `string` | `true`   |         |

### Supported Statuses

- `success`
- `failure`
- `cancelled`
- `neutral`
- `skipped`
- `timed_out`
- `action_required`

Any other status will result in a default whimsical emoji sequence.

## 💡 Outputs

| Name     | Description                               | Type     |
| :------- | :---------------------------------------- | :------- |
| `emojis` | The whimsical emoji string representing the status. | `string` |

## 🧪 Testing

The action includes a `tests/test_emojify.sh` script to verify the emoji mappings for various statuses. These tests are self-contained and do not require external dependencies or API calls.
