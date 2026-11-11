# Nightly Emoji Clock

A tiny Docker container that prints the current hour as a clock emoji.

## Usage

```sh
docker run --rm ghcr.io/your-repo/nightly-emoji-clock
```

The container will output a single emoji representing the current hour (e.g., 🕒).

You can also pass an hour (01-12) as an argument for testing:

```sh
docker run --rm ghcr.io/your-repo/nightly-emoji-clock 03
```

## Implementation

The container is based on Alpine Linux and runs a Bash script that maps the hour to one of the twelve clock face emojis.

## Testing

Run the test suite locally:

```sh
bash tests/test_emoji_clock.sh
```
