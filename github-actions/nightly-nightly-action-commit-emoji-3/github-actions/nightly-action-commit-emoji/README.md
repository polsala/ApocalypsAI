# Nightly Action Commit Emoji

A whimsical GitHub Action that maps a commit message to an emoji based on its length. Useful for adding a fun reaction in CI logs.

## Usage

```yaml
steps:
  - uses: actions/checkout@v3
  - name: Get commit message
    id: commit
    run: echo "message=$(git log -1 --pretty=%B)" >> $GITHUB_OUTPUT
  - name: Emojiify
    uses: ./github-actions/nightly-action-commit-emoji
    with:
      message: ${{ steps.commit.outputs.message }}
    id: emoji
  - run: echo "Emoji: ${{ steps.emoji.outputs.emoji }}"
```

## Inputs

- `message` (required): The commit message to evaluate.

## Outputs

- `emoji`: The selected emoji.

## How it works

The action classifies the message length:

- **< 20 characters** → 🚀 (rocket)
- **20‑50 characters** → 🌟 (star)
- **> 50 characters** → 🐢 (turtle)

Feel free to adapt the thresholds or emojis to suit your project's personality!
