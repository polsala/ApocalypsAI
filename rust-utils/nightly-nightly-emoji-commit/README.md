# Nightly Emoji Commit

A whimsical yet useful CLI that automatically prefixes conventional‑commit messages with an emoji based on the commit type. It helps you keep a colorful commit history while still following the Conventional Commits spec.

## Features

- Detects the commit type (`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`) from the first line.
- Prepends a matching emoji (`🚀`, `🐛`, `📚`, `🎨`, `🔧`, `🧪`, `🔄`).
- Leaves unknown types untouched but still adds a generic sparkle (`✨`).
- Works with a file or stdin.

## Installation

```bash
cargo install nightly-emoji-commit
```

## Usage

```bash
# From a file
nightly-emoji-commit path/to/commit.txt

# From stdin
cat commit.txt | nightly-emoji-commit
```

## Example

```text
$ cat commit.txt
feat: add new login flow

Implemented OAuth2 login with refresh token support.

$ nightly-emoji-commit commit.txt
🚀 feat: add new login flow

Implemented OAuth2 login with refresh token support.
```

## Testing

Run the test suite with:

```bash
cargo test
```

## License

MIT
