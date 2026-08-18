# Nightly Apocalypse Text Stylizer

A whimsical Node.js CLI that transforms ordinary text into a post‑apocalyptic leet‑speak version, optionally sprinkling static noise characters for extra flair.

## Installation

```sh
npm install -g .
```

## Usage

```sh
apocstylize "Hello World"
```

Outputs a stylized version, e.g.:

```
H3ll0*W0rld
```

## API

```js
import { stylize } from 'nightly-apocalypse-text-stylizer';

const result = stylize('Survive', { noise: false });
// => '5urv1v3'
```

## Options

- `noise` (boolean, default `true`): When `true`, random static characters (`~ * ^ \``) are inserted between words.

## Testing

```sh
npm test
```
