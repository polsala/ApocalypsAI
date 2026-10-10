# nightly-uptime-emoji-report

Shows system uptime with a mood‑matching emoji.

## Usage

```sh
./src/main.sh          # reads real uptime
./src/main.sh 300      # for testing: supply seconds manually
```

Outputs something like:

```
Uptime: 5 minutes 🚀
```

## Emoji mapping

- **< 1 hour** → 🚀 (fresh)
- **1 hour – 24 hours** → 😊 (content)
- **> 24 hours** → 💤 (sleepy)

## Tests

Run the test suite with:

```sh
bash tests/test_main.sh
```
