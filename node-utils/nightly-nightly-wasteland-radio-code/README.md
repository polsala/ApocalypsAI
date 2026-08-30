# nightly-wasteland-radio-code

Utility that converts plain text into a post‑apocalyptic radio code using themed words for each letter and digit. Useful for fun secret messages, role‑playing games, or adding flavor to logs.

## Installation

```sh
npm install
```

## Usage

```sh
node src/index.js "Hello World"
```

Typical output:

```
Hollow Ember Loom Loom Obsidian Wasteland Obsidian Rift Loom Dust
```

## API

```js
const { translate } = require('./src/index');
console.log(translate('ABC'));
// => "Ash Bunker Cinder"
```

## License

MIT
