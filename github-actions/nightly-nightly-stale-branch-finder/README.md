# Nightly Stale Branch Finder

A GitHub Action to identify and report stale branches in a repository, helping maintain a tidy codebase in the post-apocalyptic digital wasteland. Forgotten branches are like forgotten outposts, consuming precious resources and cluttering the landscape. This utility helps scavenge them.

## Usage

Add this action to your workflow to automatically detect stale branches.

```yaml
name: Find Stale Branches

on:
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC
  workflow_dispatch: # Allow manual triggering

jobs:
  find_stale:
    runs-on: ubuntu-latest
    permissions:
      contents: read # Required to list branches and their commits
    steps:
      - name: Find Stale Branches
        id: stale_branches_finder
        # In a real repository, replace 'polsala/ApocalypsAI/github-actions/nightly-stale-branch-finder@main'
        # with a specific release tag (e.g., @v1) for stability.
        uses: polsala/ApocalypsAI/github-actions/nightly-stale-branch-finder@main
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          days-stale: 60 # Branches not updated in 60 days are considered stale
          ignore-branches: 'main,develop,release/.*,hotfix/.*' # Comma-separated regex patterns to ignore

      - name: Output Stale Branches
        run: |
          STALE_BRANCHES=${{ steps.stale_branches_finder.outputs.stale_branches }}
          if [ "$STALE_BRANCHES" != "[]" ]; then
            echo "Found stale branches:"
            echo "$STALE_BRANCHES" | jq -r '.[]' | while read -r branch; do
              echo "- $branch"
            done
            # Example: Fail the workflow if stale branches are found
            # exit 1 
            # Example: Create an issue or comment on a PR (requires additional permissions and 'gh' CLI)
            # gh issue create --title "Stale Branches Detected" --body "Please review and delete the following branches: $STALE_BRANCHES"
          else
            echo "No stale branches found. The wasteland is clean!"
          fi
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }} # Required for `gh` CLI if used in subsequent steps
```

## Inputs

| Input Name        | Description                                                                                             | Required | Default Value           |
|-------------------|---------------------------------------------------------------------------------------------------------|----------|-------------------------|
| `github-token`    | GitHub token with `contents: read` and `pull_requests: read` permissions. Usually `${{ secrets.GITHUB_TOKEN }}`. | `true`   |                         |
| `days-stale`      | Number of days after which a branch is considered stale.                                                | `false`  | `90`                    |
| `ignore-branches` | Comma-separated list of branch patterns (regex supported) to ignore, e.g., `main,develop,release/.*`.  | `false`  | `main,master,develop`   |

## Outputs

| Output Name      | Description                                     |
|------------------|-------------------------------------------------|
| `stale-branches` | JSON array of stale branch names, e.g., `["feature/old-feature", "bugfix/forgotten-fix"]`. |

## Development & Testing

The core logic is implemented in `src/find_stale_branches.sh`. Tests are located in `tests/test_find_stale_branches.sh`.

To run tests locally:

```bash
cd github-actions/nightly-stale-branch-finder
bash tests/test_find_stale_branches.sh
```

The tests use mocks for `curl` and `date` commands to ensure determinism and avoid actual API calls.
