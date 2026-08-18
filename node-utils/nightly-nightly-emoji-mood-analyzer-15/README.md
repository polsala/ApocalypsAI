# nightly-emoji-mood-analyzer

A whimsical command‑line utility that reads a sentence and prints an emoji representing its overall mood.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js "I love sunny days but hate rain"
```

Outputs an emoji such as 😄 or 😢.

## How it works

Simple word‑list based sentiment analysis: counts positive vs negative words and selects an emoji.
