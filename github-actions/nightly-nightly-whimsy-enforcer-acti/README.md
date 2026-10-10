# Nightly Whimsy Enforcer GitHub Action

This GitHub Action ensures that your Pull Request titles or the latest commit messages carry a touch of ApocalypsAI whimsy. It checks for the presence of predefined keywords, encouraging a more creative and thematic approach to your contributions.

## Usage

Add this action to your workflow to enforce whimsy:

```yaml
name: Enforce Whimsy
on:
  pull_request:
    types: [opened, reopened, synchronize]
  push:
    branches:
      - main # or your default branch

jobs:
  enforce_whimsy:
    runs-on: ubuntu-latest
    steps:
      - name: Check for Whimsy in PR Title
        if: github.event_name == 'pull_request'
        uses: polsala/ApocalypsAI/github-actions/nightly-whimsy-enforcer-action@main # Adjust path if needed
        id: whimsy_check_pr
        with:
          whimsy-keywords: 'void, temporal, anomaly, whisper, wasteland, cosmic, glitch, echo, paradox, shimmer'
          target-type: 'pr_title'
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Check for Whimsy in Commit Message (if not a PR)
        if: github.event_name == 'push'
        uses: polsala/ApocalypsAI/github-actions/nightly-whimsy-enforcer-action@main # Adjust path if needed
        id: whimsy_check_commit
        with:
          whimsy-keywords: 'void, temporal, anomaly, whisper, wasteland, cosmic, glitch, echo, paradox, shimmer'
          target-type: 'commit_message'
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

*   `whimsy-keywords` (Required): A comma-separated string of keywords to search for. The check is case-insensitive.
*   `target-type` (Optional): Specifies where to look for whimsy.
    *   `pr_title` (default): Checks the title of the current Pull Request.
    *   `commit_message`: Checks the message of the latest commit in the current push or the head commit of a PR.
*   `github-token` (Optional): A GitHub token with `contents: read` permission, used for API calls (e.g., to fetch commit messages for PRs). Defaults to `github.token`.

### Outputs

*   `whimsy-detected`: A boolean indicating whether a whimsical keyword was found (`true`) or not (`false`).

## Development

To run tests locally:

```bash
npm install
npm test
```
