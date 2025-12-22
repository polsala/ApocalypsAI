# Nightly Void Whisperer

Adds whimsical, encouraging comments to pull requests to foster community engagement. This GitHub Action helps maintain a friendly and welcoming atmosphere by occasionally dropping a "whisper from the void" on PRs, especially for new contributors or those needing a little encouragement.

## Features

*   **Whimsical Comments**: Choose from a list of predefined or custom messages.
*   **First-Time Contributor Welcome**: Optionally targets users making their first pull request to the repository.
*   **No Comment Check**: Optionally only whispers if there are no existing human comments on the PR.
*   **Configurable Messages**: Easily customize the messages to fit your community's tone.

## Usage

To use the Nightly Void Whisperer in your workflow, add a step like this:

```yaml
name: Void Whisperer on PR

on:
  pull_request_opened:
    types: [opened, synchronize] # Trigger when a PR is opened or updated
  schedule:
    - cron: '0 0 * * *' # Run daily at midnight UTC for older PRs (optional)

jobs:
  whisper:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write # Required to post comments
    steps:
      - name: Nightly Void Whisperer
        uses: polsala/ApocalypsAI/github-actions/nightly-void-whisperer@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          messages: |
            "The void hums a tune of approval for your changes!"
            "A cosmic alignment indicates this PR is ready for review."
            "Your code is a beacon in the darkness. Keep shining!"
          trigger-on-first-pr: true
          trigger-on-no-comments: true
```

### Inputs

*   `github-token`:
    *   **Required**: `true`
    *   **Description**: Your GitHub Token. Usually `${{ secrets.GITHUB_TOKEN }}`. This token needs `pull-requests: write` permission.
*   `messages`:
    *   **Required**: `false`
    *   **Default**: A set of predefined whimsical messages.
    *   **Description**: A multiline string of messages. One will be randomly selected. Each message should be on a new line and can be enclosed in quotes.
*   `trigger-on-first-pr`:
    *   **Required**: `false`
    *   **Default**: `false`
    *   **Description**: Set to `true` to only whisper if the PR author is a first-time contributor to the repository.
*   `trigger-on-no-comments`:
    *   **Required**: `false`
    *   **Default**: `true`
    *   **Description**: Set to `true` to only whisper if the PR has no existing human comments (bot comments are ignored).

### Outputs

*   `whispered`:
    *   **Description**: `true` if a message was whispered, `false` otherwise.
*   `message`:
    *   **Description**: The specific message that was whispered (if `whispered` is `true`).

## Development

To run tests:

```bash
npm install
npm test
```

## License

This utility is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
