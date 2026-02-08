# nightly-emoji-chronometer

A tiny Rust CLI that converts a date‑time into a pair of clock‑face emojis representing the hour and, if the minutes are 30 or more, the half‑hour indicator.  If no argument is supplied the tool uses the current system time.

## Installation
```sh
# Clone the repo and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-emoji-chronometer
cargo build --release
```
The binary will be at `target/release/emoji-chronometer`.

## Usage
```sh
# Provide an RFC‑3339 timestamp (e.g. 2023-10-31T14:23:00Z)
emoji-chronometer "2023-10-31T14:23:00Z"
# → 🕑

# Minutes >= 30 add the half‑hour emoji
emoji-chronometer "2023-10-31T14:45:00Z"
# → 🕑🕜

# No argument → current local time
emoji-chronometer
```

## How it works
* The tool parses the supplied string with `chrono::DateTime::parse_from_rfc3339`.  If parsing fails it prints an error and exits with status 1.
* The hour is reduced to a 12‑hour clock and mapped to the corresponding clock‑face emoji (🕛 … 🕚).
* If the minute component is **30 or greater**, the half‑hour emoji (🕜) is appended.

## Testing
Run the unit tests with:
```sh
cargo test
```
The tests are deterministic and do not require network access.
