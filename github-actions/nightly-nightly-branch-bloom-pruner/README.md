# Nightly Branch Bloom Pruner

A GitHub Action that identifies and reports stale branches in a repository based on inactivity, helping maintain a tidy branch garden.

## 🌸 What it does

The "Branch Bloom Pruner" helps keep your repository's branch history clean and manageable. It scans all remote branches (excluding `main`, `master`, and `HEAD`), determines their last commit date, and reports any branches that haven't seen activity for a configurable number of days. This allows repository maintainers to easily identify and prune forgotten or abandoned development efforts.

## 🛠️ How to use

To integrate the Branch Bloom Pruner into your workflow, add it as a step in your GitHub Actions `.yml` file.

### Example Workflow

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
    steps:
      - name: Run Branch Bloom Pruner
        uses: polsala/ApocalypsAI/github-actions/nightly-branch-bloom-pruner@main # Replace 'main' with your branch/tag if needed
        id: pruner
        with:
          days-stale: 90 # Optional: branches inactive for 90 days are considered stale (default is 90)
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Report Stale Branches
        run: |
          STALE_BRANCHES="${{ steps.pruner.outputs.stale-branches }}"
          if [ "$STALE_BRANCHES" == "[]" ]; then
            echo "🎉 No stale branches found! Your branch garden is pristine."
          else
            echo "Found stale branches:"
            echo "$STALE_BRANCHES" | jq -r '.[]' | while read branch; do
              echo "- $branch"
            done
            # You could add further steps here, e.g.,
            # - Create an issue with the list of stale branches
            # - Post a comment on a discussion
            # - Trigger another workflow to delete branches (use with caution!)
          fi
```

## ⚙️ Inputs

| Input          | Description                                                                                             | Type    | Required | Default |
| :------------- | :------------------------------------------------------------------------------------------------------ | :------ | :------- | :------ |
| `days-stale`   | The number of days after which a branch is considered stale due to inactivity.                          | `string`| `false`  | `90`    |
| `github-token` | A GitHub token with `contents:read` permission. Typically `${{ secrets.GITHUB_TOKEN }}` is sufficient. | `string`| `true`   |         |

## 📤 Outputs

| Output           | Description                                                                 | Type     |
| :--------------- | :-------------------------------------------------------------------------- | :------- |
| `stale-branches` | A JSON array of branch names (e.g., `["feature/old-feature", "bugfix/fix-1"]`) that are considered stale. | `string` |

## 🧪 Testing

The utility includes a self-contained test script (`tests/test_prune_branches.sh`) that mocks `git` commands and the `date` command to ensure deterministic and offline testing.

To run the tests:

```bash
cd github-actions/nightly-branch-bloom-pruner
bash tests/test_prune_branches.sh
```

This will execute the test cases and report success or failure.
