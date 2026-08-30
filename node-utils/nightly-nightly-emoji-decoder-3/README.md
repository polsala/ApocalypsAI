# Nightly Emoji Decoder

Decode a sequence of emojis into a hidden alphanumeric message using a whimsical mapping.

## Installation

```sh
npm install -g nightly-emoji-decoder
```

## Usage

```sh
nightly-emoji-decoder "🍎🍌🍒"
# => ABC
```

You can also pipe input:

```sh
echo "🍉🍓🥝" | nightly-emoji-decoder
# => EFI
```

## Mapping

| Emoji | Letter |
|-------|--------|
| 🍎 | A |
| 🍌 | B |
| 🍒 | C |
| 🍇 | D |
| 🍉 | E |
| 🍓 | F |
| 🍑 | G |
| 🍍 | H |
| 🥝 | I |
| 🥭 | J |

Unmapped emojis become `?`.
