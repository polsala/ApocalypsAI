# nightly-emoji-commit-annotator

A tiny Bash utility that sprinkles a little emoji magic onto your most recent Git commit message. Perfect for adding a dash of personality to your history without leaving your terminal.

## Features

- **Random emoji**: By default picks a random emoji from a curated list.
- **Deterministic mode**: Supply `-e <emoji>` to force a specific emoji (useful for scripts or tests).
- **Safety checks**: Verifies you are inside a Git repository and that there is at least one commit.

## Installation

```bash
# Clone the repository (or copy the script into your PATH)
git clone https://github.com/polsala/ApocalypsAI.git
cp utils/bash-utils/nightly-emoji-commit-annotator/src/annotate.sh /usr/local/bin/emoji-commit
chmod +x /usr/local/bin/emoji-commit
```

## Usage

```bash
# Append a random emoji to the latest commit message
emoji-commit

# Force a specific emoji (great for CI or reproducible runs)
emoji-commit -e "🚀"
```

The script amends the **HEAD** commit (i.e., the most recent commit) by appending the emoji to the existing message, preserving the original text.

## Options

- `-e <emoji>` – Use the supplied emoji instead of a random one.
- `-h` – Show help and exit.

## License

MIT © ApocalypsAI community
