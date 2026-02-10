# nightly-emoji-chronometer

Convert a timestamp into a clock‑face emoji with minutes rounded to the nearest five minutes.

## Installation

```sh
# From the repository root
cd rust-utils/nightly-emoji-chronometer
cargo build --release
# The binary will be at target/release/emoji-chronometer
```

## Usage

```sh
emoji-chronometer 2023-10-31T14:23:00Z
```

Output:

```
🕑 25
```

The first character is the clock‑face emoji representing the hour (12‑hour clock). The number is the minutes rounded to the nearest multiple of 5 (00‑55). Invalid timestamps or missing arguments print a short usage message.

## How it works

* Parses the supplied ISO‑8601 timestamp using the `chrono` crate.
* Maps the hour (0‑23) to a 12‑hour clock emoji (🕐‑🕛).
* Rounds the minute to the nearest 5‑minute increment.
* Prints `<emoji> <MM>`.

## Testing

Run the test suite with:

```sh
cargo test
```
