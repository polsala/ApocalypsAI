# nightly-uptime-emoji-report

A whimsical Bash utility that reads the system uptime and prints an emoji representing how long the machine has been alive. Perfect for adding a touch of post‑apocalyptic flair to your terminal.

## Usage

```sh
./src/main.sh
```

Output example:

```
System uptime: 3 days 4 hours 12 minutes 🌳
```

## Emoji Legend

- 🌱 – less than 1 day
- 🌿 – 1‑3 days
- 🌳 – 3‑7 days
- 🌲 – more than 7 days

## How it works

The script reads `/proc/uptime`, converts the seconds to days, hours, and minutes, then selects an emoji based on the total days.

## Testing

Run the test suite with:

```sh
bash tests/test_main.sh
```
