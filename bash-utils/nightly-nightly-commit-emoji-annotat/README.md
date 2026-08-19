# Nightly Commit Emoji Annotator

## Overview

`nightly-commit-emoji-annotator` is a tiny Bash utility that reads your Git commit history and prefixes each entry with an emoji that hints at the commit’s purpose (feature, bug‑fix, documentation, refactor, test, chore, etc.).  It’s handy for a quick visual scan of `git log` without having to read every line.

## Installation

1. Clone the repository or copy the `src/annotate.sh` script into a directory of your choice.
2. Make it executable:
   ```bash
   chmod +x src/annotate.sh
   ```
3. (Optional) Add the script to your `PATH` or create an alias:
   ```bash
   alias git-emoji='path/to/annotate.sh'
   ```

## Usage

```bash
./src/annotate.sh
```

The script runs `git log --pretty=format:"%h %s"` in the current repository and prints each line prefixed with an appropriate emoji.

### Environment variable for testing

If you set the environment variable `GIT_LOG_MOCK`, the script will use its value instead of invoking `git`.  This is useful for automated testing or when you want to see how the script formats custom input.

```bash
export GIT_LOG_MOCK="a1b2c3 feat: add login\n d4e5f6 fix: correct typo"
./src/annotate.sh
```

## Emoji mapping

| Keyword (case‑insensitive) | Emoji |
|----------------------------|-------|
| `feat` / `feature`         | ✨    |
| `fix`                      | 🐛    |
| `docs` / `documentation`   | 📚    |
| `refactor`                 | 🔧    |
| `test`                     | ✅    |
| `chore`                    | 🧹    |
| *(any other)*              | 🔖    |

## Example output

```text
a1b2c3 ✨ feat: add user authentication
d4e5f6 🐛 fix: resolve crash on startup
7g8h9i 📚 docs: update README
```

## Testing

Run the provided test script:
```bash
cd tests && ./test_annotate.sh
```
It uses a mocked git log and verifies the emoji annotations.
