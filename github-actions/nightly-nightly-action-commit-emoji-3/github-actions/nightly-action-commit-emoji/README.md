# Commit Emoji Reactor Action

Adds a random emoji reaction to each commit in a pull request, spreading joy across the repository.

## Usage

```yaml
name: Add Emoji Reactions
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  emoji:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: React with emojis
        uses: ./github-actions/nightly-action-commit-emoji
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
```

## How it works

The action is a **composite** action that runs a small Bash script. In a real deployment it would:

1. List all commits in the PR via the GitHub API.
2. Choose a random emoji from a curated list.
3. Post a reaction to each commit.

The current implementation only prints a placeholder message for safety and offline testing.

## License

MIT
