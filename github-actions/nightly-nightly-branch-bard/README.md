# Nightly Branch Bard

A GitHub Action to help maintain a tidy repository by identifying stale branches and offering whimsical, lore-friendly suggestions for their archival or deletion. Think of it as a repository librarian, gently nudging you to clear out the forgotten scrolls and dusty tomes of your codebase.

## Features

*   **Stale Branch Detection**: Configurable threshold for identifying inactive branches.
*   **Whimsical Naming**: Generates creative, themed names for stale branches (e.g., "The Whispering Willow Branch," "The Forgotten Scroll of `feature/xyz`").
*   **Flexible Output**: Posts suggestions to the workflow summary or as a comment on a specified issue.
*   **Exclusion List**: Ignore important branches like `main` or `develop`.

## Usage

To use the Nightly Branch Bard in your workflow, add a step like this:

```yaml
name: Branch Cleanup Suggestions

on:
  schedule:
    - cron: '0 0 * * 1' # Run every Monday at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  suggest_cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository (required for context)
        uses: actions/checkout@v4

      - name: Find Stale Branches
        uses: polsala/ApocalypsAI/utils/nightly-branch-bard@main # Adjust 'main' to your branch if needed
        id: branch_bard
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          stale-days: 90 # Branches inactive for 90 days or more
          ignore-branches: 'main,develop,release/*' # Comma-separated list of branches or glob patterns to ignore
          output-type: 'summary' # or 'issue-comment'
          # issue-number: 123 # Required if output-type is 'issue-comment'

      - name: Output Stale Branches (for debugging)
        run: echo "${{ steps.branch_bard.outputs.stale-branches-json }}"
```

### Inputs

*   `repo-token`: **Required**. Your GitHub Token. Usually `${{ secrets.GITHUB_TOKEN }}`.
*   `stale-days`: **Optional**. The number of days after which a branch is considered stale. Default: `60`.
*   `ignore-branches`: **Optional**. A comma-separated string of branch names or glob patterns to ignore (e.g., `main,develop,feature/*`). Default: `main,master,develop`.
*   `output-type`: **Optional**. How to output the suggestions. Can be `summary` (default) or `issue-comment`.
*   `issue-number`: **Optional**. The issue number to comment on if `output-type` is `issue-comment`. Required if `output-type` is `issue-comment`.

### Outputs

*   `stale-branches-json`: A JSON string containing an array of identified stale branches and their whimsical suggestions. Each object includes `name`, `lastCommitDate`, and `suggestion`.
*   `summary-output`: The formatted string output that was added to the job summary or issue comment.

## Development

This action is written in JavaScript.

### Running Tests

```bash
npm install
npm test
```
