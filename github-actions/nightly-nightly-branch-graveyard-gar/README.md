# Nightly Branch Graveyard Gardener

A GitHub Action to help maintain a tidy repository by identifying and reporting stale branches. Like a diligent gardener, this action prunes the digital undergrowth, ensuring your branch graveyard doesn't become an overgrown jungle.

## 🌿 What it Does

This action scans your repository for branches that haven't received any commits for a specified number of days. It then outputs a list of these "stale" branches, allowing you to review and decide on their fate (e.g., delete, archive, or revive). It's perfect for keeping your repository clean, improving developer experience, and reducing clutter.

## ⚙️ How to Use

To integrate the Branch Graveyard Gardener into your workflow, add it to one of your `.github/workflows/*.yml` files.

```yaml
name: Branch Cleanup Check

on:
  schedule:
    - cron: '0 0 * * 1' # Run every Monday at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  identify-stale-branches:
    runs-on: ubuntu-latest
    steps:
      - name: Run Branch Graveyard Gardener
        id: pruner
        uses: polsala/ApocalypsAI/github-actions/nightly-branch-graveyard-gardener@main # Replace 'main' with your branch/tag
        with:
          stale-days: '90' # Branches older than 90 days are considered stale
          ignore-branches: 'main,master,develop,release-*' # Comma-separated list of branches/patterns to ignore

      - name: Report Stale Branches
        if: ${{ steps.pruner.outputs.stale-branches-count > 0 }}
        run: |
          echo "Found ${{ steps.pruner.outputs.stale-branches-count }} stale branches:"
          echo "${{ steps.pruner.outputs.stale-branches }}" | jq -r '.[]' | while read -r branch; do
            echo "- $branch"
          done
          # Optionally, create an issue or comment on a PR here
          # For example, to create an issue:
          # gh issue create --title "Stale Branches Detected" --body "Please review and clean up the following branches:\n${{ steps.pruner.outputs.stale-branches }}"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 📥 Inputs

*   `stale-days` (optional): The number of days after which a branch is considered stale.
    *   Default: `90`
*   `ignore-branches` (optional): A comma-separated list of branch names or patterns (using `*` for wildcards) to ignore during the scan.
    *   Default: `main,master,develop`

## 📤 Outputs

*   `stale-branches`: A JSON array of the names of all identified stale branches.
    *   Example: `["feature/old-feature", "bugfix/forgotten-fix"]`
*   `stale-branches-count`: The total number of stale branches found.

## 🧪 Testing

The action includes a self-contained test script (`tests/test_branch_pruner.sh`) that runs the core logic in a deterministic, offline manner. It uses a mock data file to simulate `git` branch information, ensuring consistent results without needing an actual Git repository or network access.

To run tests:
```bash
cd github-actions/nightly-branch-graveyard-gardener
bash tests/test_branch_pruner.sh
```
