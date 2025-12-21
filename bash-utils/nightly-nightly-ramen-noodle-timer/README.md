# nightly-ramen-noodle-timer

A tiny Bash utility that tells you the ideal cooking time for various noodle styles (ramen, udon, soba, etc.) and optionally runs a countdown timer. Perfect for the kitchen‑bound developer who likes a little automation with their broth.

## Features

- Accepts a noodle type as a positional argument.
- Prints the recommended cooking time in minutes.
- When `SKIP_SLEEP` is **not** set, sleeps for the required duration and then prints a celebratory 🍜.
- Graceful handling of unknown noodle types with a helpful usage message.

## Installation

```bash
# Clone the repository (or copy the script) and make it executable
chmod +x src/timer.sh
```

You can also add it to your `$PATH` for easy access:

```bash
sudo ln -s $(pwd)/src/timer.sh /usr/local/bin/ramen-timer
```

## Usage

```bash
./src/timer.sh <noodle-type>
```

Supported noodle types:

- `ramen` – 8 minutes
- `udon`  – 12 minutes
- `soba`  – 4 minutes
- `spaghetti` – 10 minutes
- `rice` – 18 minutes

### Example

```bash
$ ./src/timer.sh ramen
Recommended cooking time for ramen: 8 minute(s).
Waiting... (press Ctrl+C to abort)
Done! 🍜
```

If you only want the recommendation without the wait (useful for scripting), set the environment variable `SKIP_SLEEP=1`:

```bash
$ SKIP_SLEEP=1 ./src/timer.sh udon
Recommended cooking time for udon: 12 minute(s).
```

## Testing

Run the bundled test suite with:

```bash
bash tests/test_timer.sh
```

All tests should pass on any POSIX‑compatible shell.
