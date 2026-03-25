# Nightly Commit Emoji Adorner

A whimsical GitHub Action that sprinkles a random emoji onto every commit message in a pull request and posts the embellished messages as a comment. Great for adding a bit of fun flair to your PR discussions.

## Features

- Picks a random emoji from a configurable list (default includes rockets, fireworks, and more).
- Retrieves all commit messages in the PR.
- Prepends the chosen emoji to each message.
- Posts a nicely formatted comment on the PR with the emoji‑adorned messages.

## Usage

Add the following step to your workflow (e.g., `.github/workflows/emoji-adorner.yml`):

```yaml
name: Emoji Adorner
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  add-emoji:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Run Emoji Adorner
        uses: ./
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          # Optional: provide your own comma‑separated list of emojis
          # emoji-list: "🚀,✨,🔥,💡,🎉,🤖,🧩"
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github-token` | Token with permission to comment on the PR (usually `secrets.GITHUB_TOKEN`). | Yes | N/A |
| `emoji-list` | Comma‑separated list of emojis to choose from. | No | `🚀,✨,🔥,💡,🎉,🤖,🧩` |

## How it works

1. The action reads the pull request number from the GitHub context.
2. It fetches the list of commits in the PR via the GitHub REST API.
3. It selects a random emoji from the supplied list.
4. It prepends the emoji to each commit message.
5. It posts a comment on the PR containing the adorned messages.

## License

MIT © ApocalypsAI
