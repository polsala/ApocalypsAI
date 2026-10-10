# Nightly Workflow Purpose Oracle

This GitHub Action acts as a vigilant oracle, ensuring that all your GitHub Actions workflows are properly documented with a clear purpose, trigger, criticality, and a whimsical survival tip for future survivors (developers).

## 🧙‍♀️ Why use the Workflow Purpose Oracle?

In the post-apocalyptic landscape of CI/CD, clarity is paramount. This action helps maintain a self-documenting repository of workflows, making it easier for new contributors or even your future self to understand the function and importance of each automated process. No more guessing what that `mysterious-cron-job.yml` actually does!

## 📜 Oracle Entry Format

For each workflow file (`.github/workflows/*.yml`), the oracle expects a specific comment block at the top of the file. This block serves as the workflow's 'Oracle Entry' and must contain the following fields:

```yaml
# --- Workflow Oracle Entry ---
# Purpose: [Briefly describe what this workflow does, e.g., 'This workflow builds and tests the main application.']
# Trigger: [How is this workflow initiated? e.g., 'on: push', 'schedule', 'workflow_dispatch']
# Criticality: [How vital is this workflow? Choose from: Low, Medium, High, Apocalyptic]
# Survival Tip: [A whimsical tip related to the workflow's function, e.g., 'Always have a backup plan for your builds!']
# --- End Workflow Oracle Entry ---
```

**All fields must be present and non-empty.** If any field is missing or empty, the oracle will issue a warning and fail the check.

## 🚀 Usage

To integrate the Workflow Purpose Oracle into your repository, add the following step to one of your existing workflows (e.g., a daily cron job or a PR check):

```yaml
name: Workflow Documentation Check
on:
  push:
    branches:
      - main
  pull_request:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC

jobs:
  check_workflows:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run Workflow Purpose Oracle
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-purpose-oracle@main # Replace 'main' with your branch/tag
        with:
          workflow_dir: .github/workflows # Optional: default is .github/workflows
```

### Inputs

- `workflow_dir` (Optional): The directory containing GitHub Actions workflow files. Defaults to `.github/workflows`.

## 🛠️ Development & Testing

To test the action locally or during development, refer to the `tests/test_action.yml` workflow. It demonstrates how to run the action against various scenarios (valid, missing block, empty fields) and assert the expected outcomes.
