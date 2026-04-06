# nightly-wasteland-radio-code

**Convert ordinary text into a post‑apocalyptic radio code** – each alphabetic character is replaced with a themed word (e.g., `A` → `Ashen`, `B` → `Bunker`).  Spaces become `/` to separate words.

## Install & Run

The utility is a single‑file Node.js script with **no external dependencies**.  Clone the repository, then run:

```bash
node src/index.js "Your message here"
```

Example:

```bash
$ node src/index.js "Help me"
Hollow Eclipse / Mire Obsidian
```

## API

The core function is exported for programmatic use:

```js
const { encode } = require('./src/index');

const radio = encode('Stay safe');
console.log(radio); // "Scavenge Tox..."
```

## Testing

Run the bundled test script with Node:

```bash
node tests/test_main.js
```

You should see `All tests passed.` if everything is working.

## License

MIT – feel free to adapt the word list or add your own wasteland terms!
