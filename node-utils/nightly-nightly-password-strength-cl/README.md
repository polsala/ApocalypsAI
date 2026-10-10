# nightly-password-strength-cli

A whimsical CLI utility that evaluates the strength of a password and returns a fun rating with emojis.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js <password>
# or
npm start -- <password>
```

The utility reads the password from the first command‑line argument. If no argument is provided, it will read from standard input.

## Rating Scale

- **Very Weak 😱**: length < 6
- **Weak 🙈**: length ≥ 6 but contains only letters **or** only numbers
- **Moderate 😐**: length ≥ 8 with both letters and numbers
- **Strong 💪**: length ≥ 10 with letters, numbers, and symbols
- **Very Strong 🚀**: length ≥ 12 with mixed case letters, numbers, and symbols

## Examples

```sh
$ node src/index.js abc
Very Weak 😱

$ node src/index.js abcdef
Weak 🙈

$ node src/index.js abc12345
Moderate 😐

$ node src/index.js Abc12345!
Strong 💪

$ node src/index.js Abcdef12345!@
Very Strong 🚀
```

## License

MIT
