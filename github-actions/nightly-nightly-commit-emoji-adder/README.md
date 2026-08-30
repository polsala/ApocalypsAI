# Commit Emoji Adder Action

Adds emojis to PR titles based on the types of commits in the PR.

## Usage

```yaml
name: Add emojis to PR title
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  emoji:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ./  # uses this action
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

- `repo-token` (required): GitHub token with repo scope.

## How it works

The action inspects each commit message in the PR, extracts the conventional commit type (e.g., `feat`, `fix`), maps it to an emoji, and prepends the emojis to the PR title.

Supported types and emojis:

| Type | Emoji |
|------|-------|
| feat | ✨ |
| fix | 🐛 |
| docs | 📚 |
| style | 🎨 |
| refactor | ♻️ |
| test | ✅ |
| chore | 🔧 |
| perf | ⚡️ |
| build | 🏗️ |
| ci | 🤖 |
| revert | ⏪ |

## License

MIT
