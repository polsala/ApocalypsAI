# nightly-emoji-mood-analyzer

A whimsical CLI utility that reads text from **stdin** and prints an emoji representing the overall mood.

## Installation

```sh
npm install -g .
```

## Usage

```sh
echo "I am so happy today!" | node src/main.js
# 😊
```

You can also pipe the output of other commands:

```sh
cat story.txt | node src/main.js
```

## How it works

The tool uses a tiny, handcrafted word‑list for positive and negative sentiment. It counts occurrences of these words in the input and chooses an emoji:

- More positive words → 😊
- More negative words → ☹️
- Tie or none → 😐

Feel free to extend the word lists in `src/main.js` for more nuanced analysis.
