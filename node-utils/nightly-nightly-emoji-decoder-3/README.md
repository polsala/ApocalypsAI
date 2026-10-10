# nightly-emoji-decoder

Decode a sequence of emojis into a hidden alphabetic message.

## Overview

This tiny Node.js CLI maps a set of 26 emojis to the letters A‑Z. Provide a string of emojis (space‑separated or concatenated) and the tool will output the decoded text, substituting "?" for any unknown symbols.

## Installation

```sh
npm install -g nightly-emoji-decoder
```

(Or run directly with `node src/main.js`.)

## Usage

```sh
node src/main.js "😀 😃 😄"
# => ABC
```

You can also pipe input:

```sh
echo "😀😃😄" | node src/main.js
```

## Emoji Mapping

| Emoji | Letter |
|-------|--------|
| 😀   | A |
| 😃   | B |
| 😄   | C |
| 😁   | D |
| 😆   | E |
| 😅   | F |
| 😂   | G |
| 🤣   | H |
| 😊   | I |
| 😇   | J |
| 🙂   | K |
| 🙃   | L |
| 😉   | M |
| 😌   | N |
| 😍   | O |
| 🥰   | P |
| 😘   | Q |
| 😗   | R |
| 😙   | S |
| 😚   | T |
| 😋   | U |
| 😛   | V |
| 😝   | W |
| 😜   | X |
| 🤪   | Y |
| 🤩   | Z |

(Only a subset shown; full mapping is in the source code.)

## License

MIT
