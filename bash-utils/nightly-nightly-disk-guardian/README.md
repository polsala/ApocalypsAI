# nightly-disk-guardian

A whimsical Bash utility that watches your disk usage and alerts you with playful messages when it gets too full.

## Features

- Checks disk usage of a specified mount point (default `/`).
- Configurable threshold (default 80%).
- Customizable message pool for alerts.
- Works offline; can be fed mock `df` output for testing.

## Usage

```sh
./src/main.sh [-p <path>] [-t <threshold>] [-m <message_file>]
```

- `-p` path to monitor (default `/`).
- `-t` usage percentage threshold (integer, default `80`).
- `-m` file containing one message per line; a random one is chosen for alerts.

## Example

```sh
./src/main.sh -p /home -t 75 -m messages.txt
```

If usage exceeds 75%, you'll see something like:

```
⚠️  Warning! Your /home is 78% full. Time to clean up those old memes!
```

## Testing

Run the bundled tests with:

```sh
bash tests/test_main.sh
```
