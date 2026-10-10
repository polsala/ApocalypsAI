# Nightly Branch Rejuvenator

This GitHub Action is designed to prevent branches from becoming truly 'stale' or forgotten by adding a whimsical, encouraging empty commit to them after a configurable period of inactivity. It's a gentle nudge from the ApocalypsAI to keep your development garden thriving!

## Features

*   **Stale Branch Detection**: Identifies branches that haven't seen activity in a specified number of days.
*   **Whimsical Rejuvenation**: Adds an empty commit with a fun, encouraging message to the stale branch.
*   **Configurable Exclusions**: Allows you to specify branches (e.g., `main`, `master`, `develop`) that should never be rejuvenated.
*   **Output**: Provides a JSON array of all branches that were rejuvenated.

## How it Works

1.  The action fetches all remote branches.
2.  For each branch, it checks the timestamp of the last commit.
3.  If the branch's last commit is older than the `days-stale` input and it's not in the `exclude-branches` list, the action performs the following:
    *   Checks out the branch.
    *   Creates an empty commit with a randomly selected whimsical message (prefixed by `commit-message-prefix`).
    *   Pushes this new empty commit back to the branch on the remote.
4.  It then outputs a JSON array of all branches that received a rejuvenation commit.

## Usage

To use this action, add a workflow file (e.g., `.github/workflows/rejuvenate-branches.yml`) to your repository:

```yaml
name: 'Nightly Branch Rejuvenation'

on:
  schedule:
    - cron: '0 0 * * *' # Runs daily at midnight UTC
  workflow_dispatch: # Allows manual triggering

jobs:
  rejuvenate-stale-branches:
    runs-on: ubuntu-latest
    permissions:
      contents: write # Required to push commits

    steps:
      - name: Rejuvenate Stale Branches
        uses: polsala/ApocalypsAI/utils/nightly-branch-rejuvenator@main # Replace 'main' with your branch/tag if needed
        with:
          days-stale: '60' # Branches inactive for 60 days will be rejuvenated
          commit-message-prefix: 'ApocalypsAI Nudge:'
          exclude-branches: 'main,master,production,release/*'
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Check Rejuvenated Branches
        run: |
          echo "Rejuvenated branches: ${{ steps.rejuvenate-stale-branches.outputs.rejuvenated-branches }}"
```

### Inputs

| Name                    | Description                                                                 | Type     | Default                 | Required |
| :---------------------- | :-------------------------------------------------------------------------- | :------- | :---------------------- | :------- |
| `days-stale`            | Number of days after which a branch is considered stale.                    | `string` | `'30'`                  | `false`  |
| `commit-message-prefix` | Prefix for the whimsical rejuvenation commit message.                       | `string` | `'Branch Rejuvenation Protocol Activated:'` | `false`  |
| `exclude-branches`      | Comma-separated list of branch names to exclude from rejuvenation.          | `string` | `'main,master'`         | `false`  |
| `github-token`          | GitHub token with permissions to push to branches. Use `${{ github.token }}`. | `string` |                         | `true`   |

### Outputs

| Name                    | Description                                     |
| :---------------------- | :---------------------------------------------- |
| `rejuvenated-branches`  | JSON array of branch names that were rejuvenated. |

## Permissions

This action requires `contents: write` permission to be able to push new commits to your repository. Ensure your workflow has this permission granted:

```yaml
jobs:
  your-job-name:
    runs-on: ubuntu-latest
    permissions:
      contents: write # <--- IMPORTANT
    steps:
      # ...
```
