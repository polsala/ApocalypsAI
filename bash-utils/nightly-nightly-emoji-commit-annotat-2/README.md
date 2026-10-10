# Nightly Emoji Commit Annotator

A tiny Bash utility that reads commit messages from **stdin** and prefixes each line with an emoji that matches the conventional‑commit type (fix, feat, docs, etc.). Great for adding a splash of personality to `git log` output.

## Usage

```sh
git log --pretty=format:%s | ./src/emoji-annotate.sh
```

## Supported types

| Type | Emoji |
|------|-------|
| fix | 🔧 |
| feat | ✨ |
| docs | 📚 |
| refactor | ♻️ |
| test | ✅ |
| chore | 🧹 |
| *any other* | 💡 |

## Example

```sh
$ git log --pretty=format:%s -n 3
fix: correct typo
feat: add new feature
unknown change
```

```sh
$ git log --pretty=format:%s -n 3 | ./src/emoji-annotate.sh
🔧 fix: correct typo
✨ feat: add new feature
💡 unknown change
```

No external dependencies – just Bash.
