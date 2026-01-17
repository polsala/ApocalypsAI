# nightly-commit-emoji-adder

A whimsical CLI that sprinkles appropriate emojis onto your Git commit messages based on detected keywords. Makes your commit history more expressive and fun.

## Installation

```sh
# Clone the repository (or copy the folder) and install globally
npm install -g .
```

## Usage

```sh
# Pass the commit message as an argument
nightly-commit-emoji-adder "Add user authentication"
# => Add user authentication ➕

# Pipe a message via stdin
echo "Fix bug in parser" | nightly-commit-emoji-adder
# => Fix bug in parser 🛠️ 🐛
```

## Keyword → Emoji mapping

| Keyword   | Emoji |
|-----------|-------|
| fix, bug  | 🛠️ 🐛 |
| add       | ➕ |
| remove    | ❌ |
| update    | 🔄 |
| docs      | 📚 |
| test      | ✅ |
| refactor  | ♻️ |
| chore     | 🧹 |

The utility scans the commit message for these keywords (case‑insensitive) and appends the corresponding emojis (duplicates are removed).

## License

MIT © ApocalypsAI
