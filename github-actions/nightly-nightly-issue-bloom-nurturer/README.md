# Nightly Issue Bloom Nurturer

A whimsical GitHub Action designed to keep your repository's issues and pull requests vibrant and engaged. It identifies "parched" (stale) discussions and "overgrown" (too many comments) threads, then adds a friendly, nurturing comment to encourage community interaction.

## 🌸 How it Nurtures Your Digital Garden 🌸

This action periodically scans your open issues and pull requests:
- **Parched Discussions:** If an issue or PR hasn't seen activity for a specified number of days, it's considered "parched." The Nurturer will gently remind the community with a whimsical comment, encouraging fresh ideas or updates.
- **Overgrown Threads:** If a discussion accumulates too many comments without clear resolution, it's deemed "overgrown." The Nurturer will suggest a "pruning" action, like summarizing the discussion or defining next steps.

## Usage

To integrate the Issue Bloom Nurturer into your workflow, add a step like this to your `.github/workflows/your-workflow.yml` file:

```yaml
name: Nurture Issues Daily

on:
  schedule:
    - cron: '0 0 * * *' # Runs daily at midnight UTC
  workflow_dispatch: # Allows manual triggering

jobs:
  nurture:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Nurture Issues and PRs
        uses: polsala/ApocalypsAI/github-actions/nightly-issue-bloom-nurturer@main # Replace 'main' with your branch/tag
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          stale-days: 45 # Optional: Mark issues as parched after 45 days of inactivity (default: 30)
          overgrown-comment-threshold: 75 # Optional: Mark issues as overgrown after 75 comments (default: 50)
```

### Inputs

| Input                         | Description                                                                 | Required | Default |
| :---------------------------- | :-------------------------------------------------------------------------- | :------- | :------ |
| `repo-token`                  | **GitHub token for API access.** Usually `${{ secrets.GITHUB_TOKEN }}`.     | `true`   |         |
| `stale-days`                  | Number of days without activity for an issue/PR to be considered "parched". | `false`  | `30`    |
| `overgrown-comment-threshold` | Number of comments for an issue/PR to be considered "overgrown".            | `false`  | `50`    |

### Outputs

| Output             | Description                                          |
| :----------------- | :--------------------------------------------------- |
| `nurtured-items-count` | The number of issues/PRs that received a nurturing comment. |

## Development

To run tests locally:
1. Ensure Node.js is installed.
2. Navigate to the `github-actions/nightly-issue-bloom-nurturer` directory.
3. Install dependencies: `npm install`
4. Run tests: `npm test`

This action uses Node.js and the GitHub Actions toolkit.
