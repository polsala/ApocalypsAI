# Nightly Workflow Cheerleader

A GitHub Action that brings a sprinkle of joy and encouragement to your development process! This action automatically posts a whimsical, celebratory comment to a pull request or issue upon the successful completion of a workflow run.

## 🚀 How it Works

When your workflow finishes successfully, the Workflow Cheerleader springs into action. It detects the associated pull request or issue and leaves a pre-defined or custom encouraging message, boosting morale and acknowledging hard work.

## 🛠️ Usage

Add this action to any of your GitHub workflows, typically as the last step in a job that you want to celebrate.

```yaml
name: My Awesome Workflow

on:
  pull_request:
    branches: [ main ]
  push:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        run: echo "Running tests..." # Replace with your actual build/test commands

      - name: Deploy
        run: echo "Deploying..." # Replace with your actual deploy commands

      - name: 🥳 Cheer on Success!
        if: success() # Only run if previous steps succeeded
        uses: polsala/ApocalypsAI/github-actions/nightly-workflow-cheerleader@main # Adjust path if needed
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          message: "Magnificent work! The digital cosmos applauds your success!"
```

### Inputs

| Name          | Description                                                                 | Required | Default |
|---------------|-----------------------------------------------------------------------------|----------|---------|
| `token`       | **GitHub token for authentication.** Use `secrets.GITHUB_TOKEN`.            | `true`   |         |
| `message`     | **Custom cheer message.** If empty, a random whimsical message is chosen.   | `false`  |         |
| `issue-number`| **Optional issue number to comment on.** If not provided, the action attempts to find a PR or issue from the current GitHub context. | `false`  |         |

### Outputs

| Name          | Description                                 |
|---------------|---------------------------------------------|
| `comment-url` | The URL of the created comment.             |

## 🧪 Development & Testing

To test this action locally, you can use `act` or simulate the GitHub Actions environment. The `tests/test.js` file contains unit tests for the core logic, mocking GitHub API interactions.

```bash
# Install dependencies for the action's source code
npm install @actions/core @actions/github

# Run tests
npm test
```
