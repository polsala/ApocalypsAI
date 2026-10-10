# Nightly Workflow Wellness Oracle

A GitHub Action that peers into the recent history of your repository's workflows, divines their collective "wellness," and conjures a whimsical report. It helps you keep a cheerful eye on the health of your automated processes!

## 🔮 How it Works

This action fetches the workflow runs from your repository within a specified number of days. It then calculates the success rate, identifies any recent failures, and crafts a lighthearted report about the overall state of your CI/CD endeavors.

## ✨ Usage

Add this action to your workflow:

```yaml
name: Workflow Wellness Check

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  check_wellness:
    runs-on: ubuntu-latest
    steps:
      - name: Invoke the Workflow Wellness Oracle
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-wellness-oracle@main # Replace 'main' with your branch/tag
        id: oracle
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          days-to-check: 7 # Check workflows from the last 7 days

      - name: Share the Oracle's Wisdom
        run: |
          echo "The Oracle has spoken:"
          echo "${{ steps.oracle.outputs.wellness-report }}"
          # You could also post this as a comment to an issue or PR
          # For example, using another action:
          # - name: Post report as issue comment
          #   uses: actions/github-script@v6
          #   with:
          #     script: |
          #       github.rest.issues.createComment({
          #         issue_number: context.issue.number,
          #         owner: context.repo.owner,
          #         repo: context.repo.repo,
          #         body: `## Workflow Wellness Report\n\n${{ steps.oracle.outputs.wellness-report }}`
          #       })
```

## 📜 Inputs

*   `github-token`:
    *   **Required**: `string`
    *   Your GitHub Token, usually `${{ secrets.GITHUB_TOKEN }}`. This is used to authenticate API requests to fetch workflow runs.
*   `days-to-check`:
    *   **Optional**: `number`
    *   The number of past days to consider for workflow runs. Defaults to `7`.

## 🌟 Outputs

*   `wellness-report`:
    *   `string`
    *   A whimsical report summarizing the health of your recent workflows.
