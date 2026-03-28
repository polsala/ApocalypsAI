# nightly-uptime-emoji-report

Utility that prints system uptime with a whimsical emoji indicating how long the system has been up.

## Usage

```sh
./src/uptime_report.sh
```

You can override the uptime source for testing:

```sh
UPTIME_FILE=tests/mock_uptime.txt ./src/uptime_report.sh
```

## Emoji mapping

- **< 1 day**: 🌱 (seedling)
- **1‑7 days**: 🌿 (herb)
- **> 7 days**: 🌳 (tree)
