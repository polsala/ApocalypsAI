# nightly-uptime-emoji

Utility that displays the system's uptime together with a whimsical mood emoji.

## Usage

```sh
# Run against the current system uptime
./src/uptime_emoji.sh

# Provide a custom uptime string (useful for testing)
./src/uptime_emoji.sh "up 2 hours, 15 minutes"
```

The script prints a single line, for example:

```
Uptime: 2h 15m 🌞
```

## How it works

1. **Gather uptime** – By default the script calls `uptime -p` which returns a human‑readable string such as `up 2 hours, 15 minutes`.  If an argument is supplied, that string is used instead (handy for unit tests).
2. **Parse the string** – The script extracts days, hours and minutes and converts everything to total minutes.
3. **Select an emoji** based on total minutes:
   * `< 60` minutes → 🌱 (just sprouted)
   * `60‑360` minutes → 🌞 (bright and early)
   * `360‑1440` minutes → 🌆 (day‑to‑night transition)
   * `>= 1440` minutes → 🌙 (long‑lasting night)
4. **Print** the uptime in `Xh Ym` format followed by the chosen emoji.

## Why?

A quick, fun way to glance at how long a machine has been alive while getting a visual cue of its “mood”. Perfect for terminal lovers who enjoy a splash of personality.
