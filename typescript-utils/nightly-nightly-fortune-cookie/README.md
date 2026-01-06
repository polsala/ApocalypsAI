# nightly-fortune-cookie

A whimsical CLI that prints a random fortune cookie message with ASCII art.

## Installation

```bash
npm install -g nightly-fortune-cookie
```

## Usage

```bash
nightly-fortune-cookie
```

It will output a fortune and a cute ASCII cookie.

## API

```ts
import { getFortune } from 'nightly-fortune-cookie';

const fortune = getFortune();
console.log(fortune);
```

## Development

```bash
npm install
npm test
```
