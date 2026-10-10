# nightly-emoji-decoder

Decode a string of emojis into a whimsical phrase using a secret mapping.

## Installation

The utility is a single‑file Node.js script. No external dependencies are required.

```sh
# Clone the repository (or copy the files) and navigate to the utility folder
git clone https://github.com/polsala/ApocalypsAI.git
cd node-utils/nightly-emoji-decoder
```

## Usage

```sh
# Decode emojis passed as arguments
node src/main.js 🌞🔥🧟
# => sun fire zombie

# Pipe emojis via stdin
echo "🚀🛡️" | node src/main.js
# => rocket shield

# List the internal emoji‑to‑word mapping
node src/main.js --list
```

## How it works

The script contains a hard‑coded map of ten emojis to whimsical words. When decoding, each emoji character (including those that are surrogate pairs) is looked up in the map; unknown symbols are replaced with a question mark (`?`). The `--list` flag prints the full mapping.

## Testing

Run the bundled tests with Node:

```sh
node tests/test_main.js
```

All tests should pass, confirming correct decoding and mapping output.
