# nightly-epic-emoji-logger

CLI that prefixes log lines with emojis based on severity keywords.

## Usage

```bash
cat logfile | nightly-epic-emoji-logger
```

or

```bash
echo \"error: something failed\" | nightly-epic-emoji-logger
```

## How it works

The utility reads lines from stdin and prefixes each line with an emoji:

- `error` → ❌
- `warning` → ⚠️
- `info` → ℹ️
- `debug` → 🐛
- otherwise → 📜

It is useful for quickly visualizing log severity in a terminal.
