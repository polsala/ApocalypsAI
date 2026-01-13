# Nightly Emoji Mood Analyzer

A tiny Node.js commandâline utility that detects the mood of a short piece of text and prints a matching emoji.

## Features

- Simple keywordâbased mood detection (happy, sad, angry, surprised, fear, neutral)
- Zero runtime dependencies â just Node.js (v12+)
- Can be used as a global CLI or required as a module in other projects

## Installation

```bash
# Clone the repository (or copy the utility folder)
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/nightly-emoji-mood-analyzer
# Install globally (optional)
npm install -g .
```

## Usage

### As a CLI

```bash
emoji-mood "I am so happy and excited!"
# => ð
```

If you installed it globally, the command is `emoji-mood`. Otherwise you can run it with Node:

```bash
node src/index.js "I am sad about the news."
# => ð¢
```

### As a module

```javascript
const {detectMood} = require('path/to/emoji-mood-analyzer/src/index');
console.log(detectMood('Wow, that was surprising!')); // ð²
```

## How it works

The tool lowerâcases the input and checks for the presence of a small set of moodârelated keywords. The mood with the highest hit count wins; if no keywords match, it falls back to a neutral face.

## Testing

Run the bundled tests with Node:

```bash
node tests/test_index.js
```

All tests should pass, confirming deterministic behaviour.

## License

MIT â see the LICENSE file in the repository root.
