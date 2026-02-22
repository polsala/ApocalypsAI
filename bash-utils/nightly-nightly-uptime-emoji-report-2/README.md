# nightly-uptime-emoji-report

**Overview**
A tiny Bash utility that reads the system's uptime and prints a friendly emoji together with a short message describing the system's "mood".

## Usage
```bash
./src/main.sh [seconds]
```
- If you provide a numeric argument, it is interpreted as the uptime in seconds (useful for testing).
- If no argument is given, the script reads `/proc/uptime` to determine the real system uptime.

## Emoji Logic
| Uptime range | Emoji | Message |
|--------------|-------|---------|
| < 1 hour     | ☕️   | "System just woke up! Time for coffee." |
| < 1 day      | 🚀   | "System is cruising." |
| ≥ 1 day      | 🛌   | "System has been up a long time, maybe a nap?" |

## Examples
```bash
# Simulate a fresh boot (30 minutes)
./src/main.sh 1800
# Output: ☕️ System just woke up! Time for coffee.

# Simulate a typical workday (8 hours)
./src/main.sh 28800
# Output: 🚀 System is cruising.

# Real run (no argument)
./src/main.sh
# Output depends on actual uptime.
```

## Testing
Run the bundled tests with:
```bash
cd tests && ./test_main.sh
```
All tests should pass on any Unix-like system.
