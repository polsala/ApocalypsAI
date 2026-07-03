# Nightly Stale Branch Gardener

A GitHub Action that helps maintain a tidy repository by identifying and reporting stale, unmerged branches. Like a diligent gardener, it prunes away the forgotten growth, ensuring your codebase remains fresh and focused.

## 🌿 What it Does

This action scans your repository for branches that meet two criteria:
1.  **Stale**: They haven't had any new commits for a configurable number of days.
2.  **Unmerged**: They contain commits that are not present in your specified base branch (e.g., `main`).

It then outputs a JSON array of these branches, allowing you to integrate this information into further automation (e.g., creating an issue, sending a notification, or even triggering a deletion workflow).

## 🚀 Usage

To use the Stale Branch Gardener in your workflow, add the following step:

```yaml
name: Prune Stale Branches Nightly

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  identify-stale-branches:
    runs-on: ubuntu-latest
    permissions:
      contents: read # Required to checkout the repository
      pull-requests: write # If you want to create issues/PRs later
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Find Stale Branches
        id: gardener
        uses: polsala/ApocalypsAI/github-actions/nightly-stale-branch-gardener@main # Adjust path if needed
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          base_branch: 'main' # Or 'develop', 'release', etc.
          stale_days: '60' # Branches older than 60 days without new commits

      - name: Report Stale Branches
        run: |
          STALE_BRANCHES="${{ steps.gardener.outputs.stale_branches }}"
          if [ "$STALE_BRANCHES" == "[]" ]; then
            echo "✨ All clear! No stale branches found. Your garden is pristine."
          else
            echo "⚠️ Attention, Gardener! The following branches are looking a bit withered:"
            echo "$STALE_BRANCHES" | jq -r '.[] | "- " + .'
            # Example: Create an issue with the list
            # gh issue create --title "Stale Branches Detected" --body "Please review and prune: $STALE_BRANCHES"
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Required for gh CLI if creating issues
```

## ⚙️ Inputs

| Name           | Description                                                               | Required | Default |
| :------------- | :------------------------------------------------------------------------ | :------- | :------ |
| `github_token` | GitHub token with `repo` scope for API access (e.g., `${{ secrets.GITHUB_TOKEN }}`). | `true`   |         |
| `base_branch`  | The base branch to check against for merged status.                       | `false`  | `main`  |
| `stale_days`   | Number of days after which a branch is considered stale.                  | `false`  | `30`    |

## 📝 Outputs

| Name             | Description                                     |
| :--------------- | :---------------------------------------------- |
| `stale_branches` | A JSON array of stale, unmerged branch names. |

## 🧪 Testing

The action includes a self-contained test workflow (`tests/test.yml`) that uses a mocked `gh` CLI to simulate repository data. This ensures deterministic and offline testing of the action's logic without requiring actual GitHub API calls.
