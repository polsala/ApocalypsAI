# Nightly Bash Uptime Emoji

A whimsical Bash utility that displays system uptime with animated emojis and ASCII art.

## Features

- Shows system uptime in a human-readable format
- Displays animated emojis that change based on uptime duration
- Renders ASCII art based on uptime length
- Includes health check and test suite

## Installation

```bash
# Clone or copy the script to your system
chmod +x src/main.sh

# Run it
./src/main.sh
```

## Usage

```bash
# Display uptime with emoji
./src/main.sh

# Display uptime with custom emoji
./src/main.sh --emoji "🤖"

# Display uptime in verbose mode
./src/main.sh --verbose
```

## Examples

```
System Uptime: 2 days, 3 hours, 45 minutes
Emoji: 🚀
ASCII Art:
  __  __
 (  \/  )
  \    /
   \__/ 
```

## Requirements

- Bash 4.0+
- `uptime` command
- `awk` and `sed`

## License

MIT
