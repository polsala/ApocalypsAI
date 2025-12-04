# Nightly Chrono-Scribble Pad

## Whimsical Purpose
In the chaotic aftermath, even the most crucial thoughts can vanish like dust motes in a nuclear wind. The Nightly Chrono-Scribble Pad is your ephemeral memory aid, a digital parchment for those fleeting ideas, temporary reminders, and short-lived directives that don't warrant permanent archiving. Jot it down, set a decay timer, and let the winds of time naturally erase it when its purpose is served.

## Practical Usefulness
This utility allows you to:
- **Quickly capture notes**: Store short-term information without cluttering your main notes.
- **Set decay timers**: Notes can be configured to automatically expire after a specified duration (e.g., 1 hour, 1 day, 1 week).
- **Clean up automatically**: A `clean` command removes all expired notes, keeping your pad tidy.
- **List active thoughts**: See only the notes that are still relevant.

## How to Use

### Installation
This utility is self-contained. Simply navigate to the `utils/nightly-chrono-scribble-pad/src` directory.

### Commands

Run `python scribble_pad.py --help` for usage details.

- **Add a note:**
  `python scribble_pad.py add "Remember to scavenge Sector 7 before dawn." --expires-in "2h"`
  (Supported units: `s` for seconds, `m` for minutes, `h` for hours, `d` for days, `w` for weeks. Default is 24 hours if `--expires-in` is omitted.)

- **List active notes:**
  `python scribble_pad.py list`

- **Clean expired notes:**
  `python scribble_pad.py clean`

## Example Workflow

```bash
# Add a quick reminder for 30 minutes
python scribble_pad.py add "Check the perimeter sensors." --expires-in "30m"

# Add a note for a day
python scribble_pad.py add "Refuel the generator." --expires-in "1d"

# List current notes
python scribble_pad.py list

# Later, clean up expired notes
python scribble_pad.py clean

# List again to see what remains
python scribble_pad.py list
```

## Development

To run tests, navigate to the `utils/nightly-chrono-scribble-pad` directory and execute:
`python -m unittest tests/test_scribble_pad.py`
