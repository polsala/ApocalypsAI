# nightly-emoji-commit-enhancer

A whimsical GitHub Action that prepends a random emoji to the commit message of a push or pull request. Great for adding a splash of personality to your repository history.

## Usage

```yaml
uses: ./github-actions/nightly-emoji-commit-enhancer
with:
  emojis: "🚀,✨,🔥,💡" # optional, comma‑separated list
```

The action runs as a step in a workflow triggered on `push` or `pull_request`. It fetches the current commit message, selects a random emoji (or one from the provided list), and amends the commit message using `git commit --amend`. The amended commit is then force‑pushed back to the same branch.

## Inputs

- `emojis` (optional): Comma‑separated list of emojis to choose from. If omitted, a built‑in list of 20 emojis is used.

## Limitations

- Works only on repositories where the workflow has write permissions.
- Force‑pushes rewrite history; use with care on protected branches.

## License

MIT
