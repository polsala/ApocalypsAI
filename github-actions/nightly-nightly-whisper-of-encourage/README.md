# Nightly Whisper of Encouragement

A GitHub Action to sprinkle a bit of whimsical encouragement on your pull requests or issues. After a successful workflow run, this action will post a randomly selected "whisper" as a comment, boosting morale in the desolate digital landscape.

## Usage

Add this action to your workflow, typically after your build and test steps.

```yaml
name: CI/CD with Encouragement

on:
  pull_request:
    types: [opened, synchronize, reopened]
  issue_comment:
    types: [created]
    if: startsWith(github.event.comment.body, '/encourage')

jobs:
  build_and_test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test

      - name: Post Whisper of Encouragement
        if: success() # Only post if previous steps succeeded
        uses: polsala/ApocalypsAI/utils/nightly-whisper-of-encouragement@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          whispers: "The void acknowledges your effort, and it is pleased.,Even in the temporal flux, your code stands firm. Mostly.,A glitch in the matrix? No, just pure brilliance!"
```

### Inputs

*   `github-token`: **Required**. Your GitHub token, usually `${{ secrets.GITHUB_TOKEN }}`. This is used to post comments.
*   `whispers`: **Optional**. A comma-separated string of custom encouragement messages. If not provided, a set of default whimsical whispers will be used.

### Outputs

*   `whisper-chosen`: The specific whisper message that was selected and posted.

## Development

To develop and test this action locally:

1.  Clone the repository.
2.  Navigate to `utils/nightly-whisper-of-encouragement`.
3.  Install dependencies: `npm install`
4.  Run tests: `npm test`
5.  Build the action: `npm run build` (This will compile `src/index.js` into `dist/index.js`)

The `dist/index.js` file is the bundled JavaScript code that GitHub Actions executes.
