# nightly-emoji-mood-analyzer

A whimsical CLI that reads a piece of text and prints an emoji representing its overall mood. Uses a simple word‑list sentiment scoring algorithm and requires no external APIs.

## Installation

```sh
npm install -g .
# or run directly with node
```

## Usage

```sh
# Pipe text via stdin
echo "I love sunny days!" | node src/main.js
# => 😊

# Pass text as an argument
node src/main.js "I am furious about the traffic."
# => 😡
```

## How it works

- A small list of positive words adds **+1** to the score, negative words subtract **-1**.
- Final score determines the emoji:
  - **> 0** → 😊 (happy)
  - **< 0** → 😡 (angry)
  - **= 0** → 😐 (neutral)

The utility is deliberately lightweight and runs offline, making it perfect for quick mood checks in scripts or terminal fun.
