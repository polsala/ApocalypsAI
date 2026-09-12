# Nightly Branch Graveyard Keeper

A GitHub Action to identify and report on stale branches, helping maintain repository hygiene.

## 🧙‍♀️ What it does

This action scans your repository for branches that haven't been updated in a specified number of days. It then outputs a JSON array of these "stale" branch names, allowing you to integrate this information into other workflows (e.g., for reporting, manual review, or automated cleanup).

It's like a diligent groundskeeper for your repository's branch graveyard, ensuring only the lively branches remain prominent.

## 🚀 Usage

To use this action, add a step to your GitHub Actions workflow:

```yaml
name: Stale Branch Check

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  check_stale_branches:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository (optional, if you need context)
        uses: actions/checkout@v4

      - name: Find Stale Branches
        id: find_stale
        uses: polsala/ApocalypsAI/github-actions/nightly-branch-graveyard-keeper@main # Replace 'main' with your branch/tag
        with:
          stale-days: '90' # Branches older than 90 days are considered stale
          ignore-branches: 'main,master,develop,release/.*' # Comma-separated list of branches/regex to ignore

      - name: Report Stale Branches
        run: |
          STALE_BRANCHES="${{ steps.find_stale.outputs.stale-branches-json }}"
          if [ "$STALE_BRANCHES" == "[]" ]; then
            echo "🎉 No stale branches found! Repository is sparkling clean."
          else
            echo "💀 Found stale branches:"
            echo "$STALE_BRANCHES" | jq -r '.[]' # Use jq to pretty print if available
            # Example: Create an issue with the list
            # echo "::error title=Stale Branches Found::Please review the following branches: $STALE_BRANCHES"
            # gh issue create --title "Stale Branches Detected" --body "The following branches are stale: $STALE_BRANCHES" --repo "$GITHUB_REPOSITORY"
          fi
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Required for gh CLI if you use it
```

### Inputs

| Input             | Description                                                                 | Type     | Default                 | Required |
|-------------------|-----------------------------------------------------------------------------|----------|-------------------------|----------|
| `stale-days`      | Number of days after which a branch is considered stale.                    | `string` | `90`                    | `false`  |
| `ignore-branches` | Comma-separated list of branch names (or regex patterns) to ignore.         | `string` | `main,master,develop`   | `false`  |

### Outputs

| Output                | Description                                 | Type     |
|-----------------------|---------------------------------------------|----------|
| `stale-branches-json` | JSON array of stale branch names found.     | `string` |

## 🧪 Testing

The action's core logic is implemented in `src/graveyard_keeper.sh`. Unit tests for this script are located in `tests/test_graveyard_keeper.sh`. These tests use a mocked `git` environment to ensure deterministic and offline execution.

To run the tests:

```bash
cd github-actions/nightly-branch-graveyard-keeper/tests
bash test_graveyard_keeper.sh
```
