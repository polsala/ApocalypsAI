# nightly-emoji-mood-mapper

A whimsical Rust CLI that translates a textual mood into a fitting emoji with a short description. Useful for adding personality to logs, commit messages, or chat.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
emoji-mood happy
# => 😊 - Happy
```

If the mood is unknown, the tool returns `🤔 - Unknown mood`.

## Supported moods

- happy → 😊
- sad → 😢
- angry → 😠
- excited → 🤩
- tired → 😴
- confused → 🤔

## License

MIT
