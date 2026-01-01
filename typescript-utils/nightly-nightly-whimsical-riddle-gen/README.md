# nightly-whimsical-riddle-generator

Generate a whimsical riddle with an optional answer.

## Usage

```bash
npx ts-node src/main.ts
```

or

```bash
node dist/main.js
```

Add `--answer` to reveal the answer.

## Example

```bash
$ node dist/main.js
What has keys but can’t open locks?

$ node dist/main.js --answer
What has keys but can’t open locks?

Answer: A piano.
```

## Development

Run tests:

```bash
npm test
```
