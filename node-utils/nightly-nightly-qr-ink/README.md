# QR Ink

Generate QR codes as ASCII art directly from the command line.

## Installation

```sh
npm install -g .
```

## Usage

```sh
qr-ink "Hello, world!"
```

The command prints an ASCII QR code to the terminal.

## API

```js
const { generateQR } = require('qr-ink');

generateQR('some text').then(console.log);
```

## License

MIT
