# Nightly PR Cheer Bot

A whimsical GitHub Action designed to spread positivity and encouragement across your repository! This action automatically posts a random, uplifting, and often quirky comment to newly opened pull requests, ensuring every contribution starts with a smile.

## Features

*   **Automatic Encouragement:** Posts a random cheer message to new PRs.
*   **Customizable Messages:** Easily update the `src/messages.txt` file with your own unique affirmations.
*   **Positive Vibes:** Helps foster a supportive and fun development environment.

## Usage

To integrate the Nightly PR Cheer Bot into your repository, create a new workflow file (e.g., `.github/workflows/cheer-bot.yml`) and add the following configuration:

```yaml
name: PR Cheer Bot

on:
  pull_request_target:
    types: [opened, reopened]

jobs:
  cheer:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write # Required to post comments
    steps:
      - name: Post Whimsical Cheer
        uses: polsala/ApocalypsAI/nightly-pr-cheer-bot@main # Replace 'main' with your branch/tag
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: messages-file: './.github/cheer_messages.txt' # If you want to use a custom path
```

### Inputs

*   `github-token` (required): A GitHub token with `pull-requests: write` permission. Usually `${{ secrets.GITHUB_TOKEN }}`.
*   `messages-file` (optional): Path to a text file containing cheer messages, one per line. Defaults to `src/messages.txt` within the action's directory.

## Customizing Cheer Messages

You can modify the `src/messages.txt` file directly within this utility's directory, or provide your own custom file via the `messages-file` input. Each line in the file will be treated as a separate cheer message.

Example `src/messages.txt`:
```
May your code compile on the first try, and your bugs be as elusive as a temporal anomaly!
A new contribution! The cosmos aligns for your brilliance. Keep shining!
Behold, a beacon of progress! Even in the void, your efforts create light.
Remember, every line of code is a step towards a brighter, less apocalyptic future. You got this!
The ApocalypsAI Integrator observes your work with delight. Carry on, brave coder!
```

## Development & Testing

The core logic for selecting a message is in `src/get_cheer_message.sh`. You can test it locally:

```bash
# Create a dummy messages file
echo "Test message 1" > temp_messages.txt
echo "Test message 2" >> temp_messages.txt

# Run the script
bash src/get_cheer_message.sh temp_messages.txt

# Clean up
rm temp_messages.txt
```

Automated tests are provided in `tests/test_get_cheer_message.sh` to ensure the message selection works deterministically.
