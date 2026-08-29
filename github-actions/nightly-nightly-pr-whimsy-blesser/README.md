# Nightly PR Whimsy Blesser

This GitHub Action adds a touch of whimsy and encouragement to your pull request workflow. It automatically posts a random, positive, and slightly absurd blessing as a comment on pull requests that meet specific criteria (e.g., small size, specific label).

## ✨ Features

- **Conditional Blessing**: Only blesses PRs that have a configurable label (default: `bless-me`) and are within a specified line change range.
- **Random Whimsy**: Selects a random blessing from a predefined list (or a custom file).
- **Morale Booster**: Adds a lighthearted touch to the development process.

## 🚀 Usage

To use this action, add a step to your workflow, typically triggered on `pull_request_target` to allow commenting on PRs from forks securely.

```yaml
name: PR Blessing Workflow

on:
  pull_request_target:
    types: [opened, labeled, reopened, synchronize]

jobs:
  bless_pr:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write # Required to post comments on PRs
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Get PR details
        id: pr_details
        run: |
          echo "pr_number=${{ github.event.pull_request.number }}" >> "$GITHUB_OUTPUT"
          echo "pr_labels=$(jq -r '[.pull_request.labels[].name] | join(",")' "$GITHUB_EVENT_PATH")" >> "$GITHUB_OUTPUT"
          echo "pr_lines_changed=$(( ${{ github.event.pull_request.additions }} + ${{ github.event.pull_request.deletions }} ))" >> "$GITHUB_OUTPUT"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Bestow Whimsical Blessing
        id: bless_step
        uses: polsala/ApocalypsAI/utils/nightly-pr-whimsy-blesser@main # Adjust 'main' to your branch if needed
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          pr-number: ${{ steps.pr_details.outputs.pr_number }}
          pr-labels: ${{ steps.pr_details.outputs.pr_labels }}
          pr-lines-changed: ${{ steps.pr_details.outputs.pr_lines_changed }}
          # blessings-file: './.github/blessings.txt' # Optional: specify a custom blessings file path

      - name: Log Blessing Status
        if: always()
        run: |
          echo "Blessing Posted: ${{ steps.bless_step.outputs.blessing-posted }}"
          echo "Blessing Message: ${{ steps.bless_step.outputs.blessing-message }}"
```

## ⚙️ Inputs

| Name             | Description                                                              | Required | Default                 |
|------------------|--------------------------------------------------------------------------|----------|-------------------------|
| `github-token`   | GitHub token for API calls (e.g., `secrets.GITHUB_TOKEN`).               | `true`   |                         |
| `pr-number`      | The number of the Pull Request to bless.                                 | `true`   |                         |
| `pr-labels`      | Comma-separated string of labels on the Pull Request.                    | `true`   |                         |
| `pr-lines-changed` | Total number of lines added + deleted in the Pull Request.               | `true`   |                         |
| `blessings-file` | Path to a file containing one blessing per line.                         | `false`  | `src/blessings.txt`     |
| `required-label` | The label a PR must have to be considered for a blessing.                | `false`  | `bless-me`              |
| `min-lines`      | Minimum lines changed for a PR to be blessed.                            | `false`  | `1`                     |
| `max-lines`      | Maximum lines changed for a PR to be blessed.                            | `false`  | `50`                    |

## 📤 Outputs

| Name             | Description                                                              |
|------------------|--------------------------------------------------------------------------|
| `blessing-message` | The whimsical blessing message that was posted (or would have been).     |
| `blessing-posted`  | `true` if a blessing was posted, `false` otherwise.                      |

## 📝 Customizing Blessings

You can provide your own list of blessings by creating a text file (e.g., `.github/blessings.txt`) with one blessing per line and passing its path to the `blessings-file` input.

Example `blessings.txt`:
```
May your code compile on the first try, and your tests always pass!
Behold, a PR worthy of a thousand rubber ducks!
Your commits are like tiny, sparkling gems in the vast ocean of git history.
```

## 🧪 Testing

Refer to `tests/test_action.yml` for examples of how this action is tested. The tests mock GitHub context inputs to ensure the logic for label checking, size validation, and blessing selection works as expected without making actual API calls.
