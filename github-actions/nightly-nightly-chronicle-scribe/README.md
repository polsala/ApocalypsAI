# Nightly Chronicle Scribe

## Whimsical Utility: The Chronicle Scribe

In the post-apocalyptic landscape, keeping track of changes is paramount. The "Chronicle Scribe" is a diligent GitHub Action that automatically records significant events (merged Pull Requests) into your project's `CHRONICLE.md` (or any specified file). It ensures that your project's history is always up-to-date, without requiring manual intervention, freeing up your survivors for more pressing tasks like scavenging for temporal anomalies.

## Features

*   **Automated Entry Creation**: Automatically generates new entries for merged Pull Requests.
*   **Customizable Format**: Define your own entry format using placeholders for PR title, number, author, and merge date.
*   **Flexible Chronicle File**: Specify the path to your chronicle file (e.g., `CHANGELOG.md`, `HISTORY.md`).
*   **Self-Updating**: Commits the updated chronicle file directly back to the repository.

## Usage

To use the Chronicle Scribe, add it as a step in your GitHub Actions workflow. It should typically run on `pull_request` events with `types: [closed]` and conditionally execute only when the PR has been merged.

### Example Workflow (`.github/workflows/update-chronicle.yml`):

```yaml
name: Update Project Chronicle

on:
  pull_request:
    types: [closed]

jobs:
  update_chronicle:
    # Only run if the pull request was merged
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        # IMPORTANT: Use a token with write permissions. 
        # For actions that commit back to the repo, you might need a PAT or specific permissions.
        # The default GITHUB_TOKEN usually has write permissions for the current repo.
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Chronicle Scribe
        # Replace 'polsala/ApocalypsAI' with your repository path if forking, 
        # or adjust if you move this action within your repo.
        uses: polsala/ApocalypsAI/github-actions/nightly-chronicle-scribe@main 
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          chronicle-file: 'CHRONICLE.md'
          entry-format: '* {PR_TITLE} (#{PR_NUMBER}) by @{PR_AUTHOR} on {MERGE_DATE}'
          commit-message: 'docs: Chronicle update for PR #{PR_NUMBER}'

      - name: Output new chronicle entry
        run: echo "New entry: ${{ steps.chronicle-scribe.outputs.chronicle-entry }}"
```

## Inputs

| Name             | Description                                                                                             | Required | Default                      |
| :--------------- | :------------------------------------------------------------------------------------------------------ | :------- | :--------------------------- |
| `github-token`   | **Required.** GitHub token with write permissions for the repository. Usually `${{ secrets.GITHUB_TOKEN }}`. | `true`   |                              |
| `chronicle-file` | Path to the chronicle file to update.                                                                   | `false`  | `CHRONICLE.md`               |
| `entry-format`   | Template string for the new chronicle entry. Placeholders: `{PR_TITLE}`, `{PR_NUMBER}`, `{PR_AUTHOR}`, `{MERGE_DATE}`. | `false`  | `* {PR_TITLE} (#{PR_NUMBER}) by @{PR_AUTHOR} on {MERGE_DATE}` |
| `commit-message` | Commit message for the chronicle update. Placeholders: `{PR_NUMBER}`.                                   | `false`  | `docs: Chronicle update for PR #{PR_NUMBER}` |

## Outputs

| Name              | Description                               |
| :---------------- | :---------------------------------------- |
| `chronicle-entry` | The new entry that was added to the chronicle file. |

## Development

This action is written in JavaScript/Node.js. Dependencies are managed via `package.json`.
