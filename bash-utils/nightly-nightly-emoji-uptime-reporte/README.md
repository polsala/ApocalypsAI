# nightly-emoji-uptime-reporter

A whimsical Bash utility that displays system uptime using emojis for days, hours, and minutes.

## Usage

```sh
./src/emoji_uptime.sh
```

You can also provide a fake uptime (in seconds) via the `FAKE_UPTIME` environment variable for testing:

```sh
FAKE_UPTIME=90061 ./src/emoji_uptime.sh
```

## Output

The script prints:

```
Uptime: <days>🌞 <hours>⏰ <minutes>🕒
```

Example:

```
Uptime: 2🌞 5⏰ 30🕒
```

## How it works

- Reads `/proc/uptime` (or `FAKE_UPTIME` if set) to get total seconds.
- Converts seconds to days, hours, minutes.
- Maps each unit to an emoji.
