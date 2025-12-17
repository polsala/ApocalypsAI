# nightly-ansi-echo

A whimsical Bash utility that echoes your message in a deterministic ANSI color and logs it with a timestamp.

## Usage

```bash
./src/ansi_echo.sh "Your message here"
```

If no argument is given, the script reads from standard input.

The script writes the message to `ansi_echo.log` in the current directory, prefixed with a timestamp.
