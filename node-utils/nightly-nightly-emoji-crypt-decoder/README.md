# Nightly Emoji Crypt Decoder

## Overview

`nightly-emoji-crypt-decoder` translates a string of emojis into plainâtext letters using a predefined substitution cipher.  Itâs perfect for fun puzzles, secret messages, or adding a whimsical touch to community posts.

## Installation

The utility is a pure Node.js script with no external dependencies.  Clone the repository (or copy the `src/` folder) and run it with Node 14+:

```bash
node src/main.js "ððð"
```

You can also pipe input:

```bash
echo "ððð" | node src/main.js
```

## Emoji â Letter Mapping

| Emoji | Letter | Emoji | Letter |
|-------|--------|-------|--------|
| ð | A | ð | H |
| ð | B | ð¥ | I |
| ð | C | ð | J |
| ð | D | ð¥ | K |
| ð | E | ð | L |
| ð | F | ð¥ | M |
| ð | G | ð¥ | N |
| ð | H | ð½ | O |
| ð¥ | I | ð¶ï¸ | P |
| ð | J | ð§ | Q |
| ð¥ | K | ð§ | R |
| ð | L | ð | S |
| ð¥ | M | ð¥ | T |
| ð¥ | N | ð | U |
| ð½ | O | ð¥ | V |
| ð¶ï¸ | P | ð§ | W |
| ð§ | Q | ð | X |
| ð§ | R | ð | Y |
| ð | S | ð¥© | Z |

Any emoji not listed in the table is decoded as `?`.

## Usage

```bash
# Decode via argument
node src/main.js "ððð"
# => ABC

# Decode via stdin
echo "ððð" | node src/main.js
# => ABC
```

## Testing

Run the bundled test script with Node:

```bash
node tests/test_main.js
```

You should see `All tests passed` if everything works correctly.

