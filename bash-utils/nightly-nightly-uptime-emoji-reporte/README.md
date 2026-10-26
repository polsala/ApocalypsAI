# nightly-uptime-emoji-reporter

A whimsical Bash utility that translates system uptime into an emoji, giving you a quick visual cue of how long your machine has been running.

## Usage

```sh
./src/uptime_emoji.sh          # reads actual system uptime
./src/uptime_emoji.sh 3600     # for testing: provide uptime in seconds
```

## Emoji mapping

- `< 1 hour` → 🚀 (fresh start)
- `< 1 day` → 🌞 (bright)
- `< 7 days` → 🌤 (steady)
- `< 30 days` → 🌧 (getting tired)
- `≥ 30 days` → 🐢 (slow and steady)

## Installation

Copy the utility into your repo, make it executable:

```sh
chmod +x src/uptime_emoji.sh
```

## Testing

Run the provided tests with Bash:

```sh
bash tests/test_uptime_emoji.sh
```
