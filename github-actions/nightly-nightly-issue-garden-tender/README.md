# Nightly Issue Garden Tender

A whimsical GitHub Action that helps maintain a healthy "issue garden" by gently reminding contributors to "water" (comment on) stale issues. It identifies open issues that haven't seen activity in a specified number of days and posts a friendly reminder, optionally adding a label to prevent repeated watering.

## 🌱 How it works

1.  **Scans for Thirsty Plants**: The action fetches all open issues in your repository.
2.  **Checks for Stale-ness**: It determines if an issue is "stale" based on its `updated_at` timestamp (which reflects comments, edits, etc.) and a configurable `stale_days` threshold.
3.  **Ignores Specific Weeds**: You can configure it to ignore issues with certain labels (e.g., `bug`, `enhancement`) that might have different lifecycle expectations.
4.  **Avoids Over-Watering**: Issues that have already been "watered" by this action (identified by a specific `action_label`) are skipped.
5.  **Posts a Reminder**: For each truly stale issue, it posts a configurable whimsical comment, encouraging community engagement.
6.  **Marks as Watered**: It then adds the `action_label` to the issue to prevent it from being watered again until further activity occurs.

## 🚀 Usage

Create a new workflow file (e.g., `.github/workflows/issue-garden.yml`) in your repository:

```yaml
name: Issue Garden Tender

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  tend_garden:
    runs-on: ubuntu-latest
    permissions:
      issues: write # Required to comment on issues and add labels
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Tend to the Issue Garden
        uses: polsala/ApocalypsAI/utils/nightly-issue-garden-tender@main # Replace 'main' with your branch if needed
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          stale_days: '60' # Issues inactive for 60 days are considered thirsty
          watering_message: 'This issue plant is looking a bit parched! 🌵 Can anyone help give it some love and attention?'
          labels_to_ignore: 'bug,documentation,wontfix' # Don't water issues with these labels
          action_label: 'garden-tender-watered' # Label to mark issues that have been watered
          dry_run: 'false' # Set to 'true' to only log actions without posting comments or adding labels
```

### Inputs

| Input Name         | Description                                                                                             | Required | Default Value                                                                                                                             |
| :----------------- | :------------------------------------------------------------------------------------------------------ | :------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| `github_token`     | **Required.** GitHub token with `issues:write` permission. Usually `${{ secrets.GITHUB_TOKEN }}`.       | `true`   |                                                                                                                                           |
| `stale_days`       | Number of days after which an issue is considered stale (no activity).                                  | `false`  | `30`                                                                                                                                      |
| `watering_message` | The whimsical message to post on stale issues.                                                          | `false`  | `This little issue plant looks a bit thirsty! 💧 Any kind gardener willing to give it some attention?`                                   |
| `labels_to_ignore` | Comma-separated list of labels to ignore (e.g., `bug,enhancement`). Issues with these labels will not be watered. | `false`  | `""`                                                                                                                                      |
| `action_label`     | The label to add to issues after they have been "watered" to prevent re-watering.                       | `false`  | `garden-tender-watered`                                                                                                                   |
| `dry_run`          | If `true`, the action will only log what it *would* do without posting comments or adding labels.       | `false`  | `false`                                                                                                                                   |

## 🧪 Testing

The action includes a self-contained test workflow (`tests/test.yml`) that uses a mocked `gh` CLI to simulate GitHub API responses. This ensures deterministic and offline testing of the action's logic without making actual API calls.

To run the tests, you can trigger the `Test Nightly Issue Garden Tender` workflow manually or push changes to the repository. The test workflow will:
1.  Set up a mock `gh` CLI that returns predefined issue data.
2.  Run the `nightly-issue-garden-tender` action in a `dry_run` mode and verify that it correctly identifies stale issues.
3.  Run the action again in a non-`dry_run` mode and verify that it logs the "watering" and "labeling" actions.

The mock `gh` CLI is configured to return a specific set of issues, including:
-   A stale issue that should be watered.
-   A fresh issue that should be ignored.
-   An issue with an ignored label.
-   An issue already marked as "watered".
-   Another stale issue that should be watered.

This setup allows for comprehensive testing of the filtering and action logic.
