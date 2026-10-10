# nightly-emoji-chronometer

**nightly-emoji-chronometer** is a tiny TypeScript command‑line utility that prints the current time where each digit is replaced by its corresponding emoji.  It’s perfect for adding a splash of fun to your terminal or scripts.

## Features
- Shows hours, minutes, and seconds as emojis (e.g., `12:34:56` → `1️⃣2️⃣🕛3️⃣4️⃣🕒5️⃣6️⃣`).
- Works on any platform with Node.js.
- Zero runtime dependencies – just the Node standard library.

## Installation
```bash
# Using npm (or yarn/pnpm)
npm install -g ts-node typescript
# Then link the utility (optional)
npm link
```

## Usage
```bash
# Run directly with ts-node
npx ts-node src/main.ts

# After global install (if you linked it)
emoji-chronometer
```

The output will look something like:
```
🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛
```
*(the exact emojis depend on the current time)*

## Development
```bash
# Install dev dependencies (jest for testing)
npm install --save-dev jest @types/jest ts-jest

# Run tests
npm test
```

## License
MIT © ApocalypsAI Community
