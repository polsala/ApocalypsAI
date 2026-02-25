# nightly-emoji-moodboard

**nightly‑emoji‑moodboard** is a tiny Rust command‑line utility that turns mood words into a playful emoji moodboard.  It’s perfect for adding a splash of personality to social‑media posts, commit messages, or just for fun.

## Features

- Accepts one or more mood keywords (e.g., `happy`, `sad`, `energetic`).
- Maps each mood to a curated list of emojis.
- Randomly picks an emoji for each supplied mood.
- If no moods are supplied, it generates a random three‑emoji board.

## Installation

```bash
# Clone the repository (or copy the generated folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-emoji-moodboard

# Build the binary
cargo build --release
```

The compiled binary will be located at `target/release/nightly-emoji-moodboard`.

## Usage

```bash
# Provide your own moods
./nightly-emoji-moodboard happy relaxed productive
# Example output: 😄 🧘‍♂️ 🚀

# No arguments → random three‑emoji board
./nightly-emoji-moodboard
# Example output: 🌟 🍕 🎉
```

## Testing

```bash
cargo test
```

All tests run offline and are deterministic.

## License

MIT © ApocalypsAI
