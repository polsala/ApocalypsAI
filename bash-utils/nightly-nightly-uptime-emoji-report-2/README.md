# nightly-uptime-emoji-report

Utility that displays the system's uptime accompanied by a whimsical emoji representing how long the machine has been running.

## Usage

```sh
./src/main.sh
```

You can also override the detected uptime for testing or fun:

```sh
MOCK_UPTIME=90000 ./src/main.sh   # 25 hours
```

## Emoji Legend

- 🌱 less than 1 day
- 🌿 1‑7 days
- 🌳 7‑30 days
- 🏜️ more than 30 days
