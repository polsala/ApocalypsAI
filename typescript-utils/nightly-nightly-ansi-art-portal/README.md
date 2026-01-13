# nightly-ansi-art-portal

A whimsical CLI utility that turns any text into colorful ASCII art using ANSI escape codes. Perfect for spicing up terminal output, README banners, or just having fun with your shell.

## Features

- Supports AâZ and space (other characters are rendered as blanks)
- Randomly colors each character with red, green, or yellow
- Deterministic output when a `--seed` is supplied (useful for testing)
- Zeroâdependency TypeScript implementation (runs with `ts-node` or after compilation)

## Installation

```sh
npm install -g ts-node typescript   # if you don't have them
git clone <repo-url>
cd utils/nightly-ansi-art-portal
npm install
```

## Usage

```sh
npx ts-node src/main.ts "Hello World"          # random colors
npx ts-node src/main.ts "Hello" --seed 42      # deterministic colors
```

The output will be printed to stdout with ANSI color codes.

## Example

````
$ npx ts-node src/main.ts "A"
[32m  #  [0m 
[33m # # [0m 
[31m#####[0m 
[32m#   #[0m 
[33m#   #[0m 
````

## License

MIT

