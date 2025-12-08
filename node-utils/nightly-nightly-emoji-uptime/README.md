# nightly-emoji-uptime

A whimsical Node.js CLI that prints your system's uptime with friendly emojis.

## Usage

```bash
npx nightly-emoji-uptime
```

or install globally:

```bash
npm i -g nightly-emoji-uptime
emoji-uptime
```

The command outputs something like:

```
🟢 Uptime: 3 days 4 hours 12 minutes 5 seconds
```

## Features

- Cross‑platform (Linux, macOS, Windows)
- No external dependencies
- Simple, deterministic output
- Exported `getUptimeMessage(seconds)` function for programmatic use

## Testing

Run the test suite with:

```bash
npm test
```
