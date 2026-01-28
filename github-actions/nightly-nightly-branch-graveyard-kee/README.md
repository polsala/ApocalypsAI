# Nightly Branch Graveyard Keeper

This GitHub Action helps maintain a tidy repository by identifying branches that haven't seen activity for a specified period. Instead of just listing them, it offers whimsical suggestions for how to deal with these "stale" branches, turning repository cleanup into a delightful, if slightly spooky, task.

## 👻 What it Does

- Fetches all branches in your repository.
- Determines the last commit date for each branch.
- Flags branches as "stale" if their last commit is older than a configurable number of days.
- Ignores specified branches (e.g., `main`, `develop`).
- Provides a report of stale branches along with a unique, whimsical suggestion for each.

## 🧙‍♀️ Whimsical Suggestions

The action will offer one of these delightful directives for each forgotten branch:
- "Offer it to the Code Goblins for recycling!"
- "Reanimate it with a fresh commit, if it still breathes!"
- "Archive it to the Digital Dustbin, where old code sleeps!"
- "Perform a ritual merge, if its spirit still aligns!"
- "Let it drift into the Void of Unmaintained Features!"

## 🚀 Usage

To use the Nightly Branch Graveyard Keeper, add a step to your workflow file (e.g., `.github/workflows/cleanup.yml`):

```yaml
name: Branch Graveyard Cleanup

on: 
  schedule:
    - cron: '0 0 * * *' # Runs daily at midnight UTC
  workflow_dispatch: # Allows manual triggering

jobs:
  identify-stale-branches:
    runs-on: ubuntu-latest
    permissions:
      contents: read # Required to list branches
    steps:
      - name: Checkout repository (optional, if you need other actions)
        uses: actions/checkout@v4

      - name: Run Branch Graveyard Keeper
        id: graveyard-keeper
        uses: polsala/ApocalypsAI/.github/actions/nightly-branch-graveyard-keeper@main # Adjust path if this action is moved
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          stale-days: 90 # Branches older than 90 days are considered stale
          ignore-branches: 'main,master,develop' # Comma-separated list of branches to ignore

      - name: Report Stale Branches
        if: steps.graveyard-keeper.outputs.stale-branches-count > 0
        run: |
          echo "Found ${{ steps.graveyard-keeper.outputs.stale-branches-count }} stale branches:"
          echo "${{ steps.graveyard-keeper.outputs.stale-branches-report }}" | jq .
          # You can add further steps here, e.g., open an issue or comment on a PR
          # For example, to open an issue:
          # gh issue create --title "Stale Branches Detected by Graveyard Keeper" \
          #   --body "The following branches are stale:\n```json\n${{ steps.graveyard-keeper.outputs.stale-branches-report }}\n```"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Required for gh CLI if used
```

### Inputs

| Name              | Description                                                               | Required | Default     |
|-------------------|---------------------------------------------------------------------------|----------|-------------|
| `repo-token`      | GitHub token with `contents: read` permission.                            | Yes      |             |
| `stale-days`      | Number of days after which a branch is considered stale.                  | No       | `90`        |
| `ignore-branches` | Comma-separated list of branch names to ignore (e.g., `main,develop`).    | No       | `main,master` |

### Outputs

| Name                      | Description                                                               |
|---------------------------|---------------------------------------------------------------------------|
| `stale-branches-count`    | The total number of stale branches found.                                 |
| `stale-branches-report`   | A JSON string array of objects, each containing `branchName`, `lastCommitDate`, `ageDays`, and `whimsicalSuggestion`. |

## 🛠️ Development

This action is written in JavaScript/Node.js.
