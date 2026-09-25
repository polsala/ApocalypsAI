# nightly-emoji-mood-analyzer

A tiny Node.js utility that reads a short piece of text and returns an emoji representing the overall mood. Perfect for adding a splash of personality to logs, commit messages, or chat bots.

## Installation

```sh
npm install -g .
# or just run with node
```

## Usage

```sh
node src/main.js "I love sunny days!"
# => 😊
```

You can also pipe text:

```sh
echo "I am so frustrated with this bug" | node src/main.js
# => 😠
```

## How it works

The analyzer uses a handcrafted list of positive, negative, and angry words. Each occurrence adjusts a score, which is then mapped to an emoji:

- score ≥ 2 → 😊 (happy)
- score ≤ -2 → 😠 (angry)
- -1 ≤ score < 2 → 😞 (sad)
- otherwise → 😐 (neutral)

## Testing

Run the bundled tests with:

```sh
node tests/test_main.js
```
