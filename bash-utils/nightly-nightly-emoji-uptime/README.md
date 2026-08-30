# nightly-emoji-uptime

**Utility:** Displays the system's uptime in a human‑readable format decorated with emojis.

## Features

- Parses the system uptime (seconds) and converts it into days, hours, and minutes.
- Adds playful emojis:
  - 📅 for days
  - 🕒 for hours
  - ⏱️ for minutes
- Works as a standalone script or can be sourced for programmatic use.

## Installation

Copy the `src/main.sh` script to a location in your `$PATH` and make it executable:

```bash
mkdir -p ~/.local/bin
cp src/main.sh ~/.local/bin/emoji-uptime
chmod +x ~/.local/bin/emoji-uptime
```

## Usage

```bash
# Default: reads the actual system uptime
emoji-uptime

# For testing or custom values, pass the uptime in seconds
emoji-uptime 90061   # => "Uptime: 1📅 1🕒 1⏱️"
```

## Example Output

```
Uptime: 3📅 5🕒 12⏱️
```

## Testing

Run the bundled test suite with:

```bash
cd tests && ./test_main.sh
```

All tests should pass.
