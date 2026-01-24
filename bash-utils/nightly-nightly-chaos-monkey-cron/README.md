# nightly-chaos-monkey-cron

A playful Bash utility that injects harmless chaos into your terminal sessions at random intervals. Designed for fun and mild annoyance, it helps keep you alert during long coding sessions.

## Features

- Randomly triggers silly terminal effects like fake typos, emoji storms, or delayed prompts
- Configurable via environment variables
- Safe and non-destructive

## Usage

```bash
# Run manually
./src/chaos.sh

# Schedule with cron to surprise yourself periodically
# Add this line to your crontab (crontab -e)
*/15 * * * * CHAOS_MODE=random DISPLAY=:0 /path/to/src/chaos.sh
```

## Environment Variables

- `CHAOS_MODE`: Set to `typo`, `emoji`, `delay`, or `random` (default)
- `CHAOS_CHANCE`: Integer from 0-100; chance of chaos per run (default: 30)

## Example Output

```
Oops! Did I type that right? 😅
```
