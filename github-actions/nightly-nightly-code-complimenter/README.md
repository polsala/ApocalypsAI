# Nightly Code Complimenter Action

This GitHub Action brings a dose of positivity to your code review process by posting a randomly generated, whimsical compliment on every new or updated pull request. Because every line of code deserves a little love!

## ✨ Features

*   **Whimsical Compliments:** A curated list of encouraging and fun messages.
*   **Automated Feedback:** Posts comments directly on your pull requests.
*   **Easy Integration:** Simple to add to any GitHub Actions workflow.

## 🚀 Usage

To use the Nightly Code Complimenter, add a step to your existing pull request workflow or create a new one like this:

```yaml
# .github/workflows/compliment.yml
name: Code Complimenter

on:
  pull_request:
    types: [opened, reopened, synchronize]

jobs:
  compliment:
    runs-on: ubuntu-latest
    steps:
      - name: Give a Code Compliment
        uses: polsala/ApocalypsAI/.github/actions/nightly-code-complimenter@main # Adjust path if this action is moved
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          pr_number: ${{ github.event.pull_request.number }}
          repo_full_name: ${{ github.repository }}
          # Optional: compliment_type: 'general' # Can be extended to 'refactor', 'new-feature', etc.
```

### Inputs

*   `github_token` (Required): Your GitHub Token, usually `${{ secrets.GITHUB_TOKEN }}`. This is used to authenticate with the GitHub API to post comments.
*   `pr_number` (Required): The number of the pull request. Use `${{ github.event.pull_request.number }}`.
*   `repo_full_name` (Required): The full name of the repository (e.g., `octocat/hello-world`). Use `${{ github.repository }}`.
*   `compliment_type` (Optional): A string to hint at the type of compliment desired. Currently, only 'general' is supported, but this input is reserved for future expansion to allow more context-aware compliments. Default: `general`.

## 🛠️ How It Works

The action executes a simple bash script that selects a random compliment from an internal list. It then uses the provided `github_token` to authenticate and post this compliment as a new comment on the specified pull request via the GitHub API.

## 🧪 Testing

The action includes a self-contained test script (`tests/test_complimenter.sh`) that mocks the `curl` command to simulate API calls without actual network interaction. This ensures deterministic and offline testing.
