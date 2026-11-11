# nightly-ruin-cryptographer

Utility to encode and decode messages using a post‑apocalyptic Caesar cipher with a custom rune alphabet. Useful for secret notes among survivors.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/main.js encode "HELLO WORLD"
# => MJQQT BTWQI

node src/main.js decode "MJQQT BTWQI"
# => HELLO WORLD
```

## API

```js
const { encode, decode } = require('./src/main');

encode('HELLO'); // => 'MJQQT'
decode('MJQQT'); // => 'HELLO'
```

## License

MIT
