# Nightly Commit Emoji Enhancer

A whimsical GitHub Action that appends a random emoji to each commit message during CI runs, adding a splash of personality to your repository history.

## Usage

```yaml
name: Enhance Commits
on:
  push:
    branches: [main]

jobs:
  emoji:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Add Emoji to Commit Message
        uses: ./
        id: enhancer
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Show Result
        run: echo "New message: ${{ steps.enhancer.outputs.new_message }}"
```

The action reads the latest commit message, appends a random emoji, and sets the output `new_message`. It also creates a new commit with the enhanced message if you enable `commit: true`.

## Inputs

- `commit` (optional, default `false`): Whether to create a new commit with the enhanced message.

## Outputs

- `new_message`: The commit message after emoji enhancement.

## License

MIT
