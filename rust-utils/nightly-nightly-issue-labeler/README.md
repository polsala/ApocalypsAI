# nightly-issue-labeler

A whimsical yet useful Rust CLI that suggests GitHub issue labels based on the issue body. It scans for common keywords and outputs a comma‑separated list of labels.

## Usage

```bash
# Read from stdin
echo "This is a bug that crashes the app" | nightly-issue-labeler

# Read from a file
nightly-issue-labeler issue.txt
```

## How it works

The tool looks for the following keywords (case‑insensitive):

- `bug` → `bug`
- `feature` → `enhancement`
- `documentation` → `documentation`
- `question` → `question`
- `performance` → `performance`
- `security` → `security`

It outputs the matched labels in the order they appear in the keyword list.

## Example

```bash
$ echo "Feature request: add dark mode" | nightly-issue-labeler
enhancement
```

## License

MIT
