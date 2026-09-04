# Nightly PR Ponderer

Adds a whimsical, thought-provoking question as a comment to new or updated Pull Requests to encourage deeper reflection and engagement.

## Usage

To use the PR Ponderer, add it as a step in your GitHub Actions workflow. It's typically triggered on `pull_request` events.

```yaml
name: PR Pondering

on:
  pull_request:
    types: [opened, synchronize] # Trigger on new PRs or when PRs are updated

jobs:
  ponder:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Add a pondering question to the PR
        uses: polsala/ApocalypsAI/nightly-pr-ponderer@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: questions-file: '.github/my_custom_questions.txt'
```

## Inputs

*   `github-token`: **Required**. A GitHub token with `pull_requests: write` permission to post comments. Usually `${{ secrets.GITHUB_TOKEN }}`.
*   `questions-file`: *Optional*. Path to a custom file containing questions, one per line. If not provided, it defaults to `.github/pr_ponderer_questions.txt` within the repository, or uses a set of built-in default questions if that file is not found or is empty.

## Example `questions-file` (`.github/pr_ponderer_questions.txt`)

```
What if the universe is just a giant simulation, and this PR is a critical patch?
Have you considered the existential implications of this code's future maintenance?
If a tree falls in the forest and no one reviews its PR, does it still merge?
Does this PR spark joy, or merely fix a bug?
```

## How it Works

The action extracts the Pull Request number from the `GITHUB_REF` environment variable. It then reads questions from the specified `questions-file` (or uses built-in defaults). A random question is selected and posted as a new comment on the Pull Request using the GitHub CLI (`gh api`).
