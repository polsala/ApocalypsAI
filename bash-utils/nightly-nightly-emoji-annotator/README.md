# nightly-emoji-annotator

A whimsical Bash utility that appends a context‑aware emoji to a line of text. It scans the input for known keywords (e.g., "fix", "feat", "doc") and attaches a matching emoji; if no keyword matches, it adds a neutral smiley. Useful for spicing up commit messages, chat lines, or any short text.

## Usage

```sh
echo "Add new feature for user login" | ./src/emoji_annotator.sh
# Output: Add new feature for user login 🚀
```

## Keywords

- fix → 🛠️
- bug → 🛠️
- feat → 🚀
- feature → 🚀
- doc → 📚
- docs → 📚
- test → ✅
- tests → ✅
- refactor → ♻️
- chore → 🧹

If none of the above keywords are present, a neutral smiley (🙂) is appended.

## Installation

Just copy the script and make it executable:

```sh
chmod +x src/emoji_annotator.sh
```

## License

MIT
