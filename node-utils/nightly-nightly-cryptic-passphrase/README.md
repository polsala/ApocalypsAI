# nightly-cryptic-passphrase

Generate post‑apocalyptic themed passphrases for secure passwords.

## Installation

```sh
npm install -g .
```

## Usage

```sh
node src/index.js -c 5 -d _
```

Options:
- `-c`, `--count` Number of words in the passphrase (default: 4)
- `-d`, `--delimiter` String used to join the words (default: `-`)

## Example

```sh
$ node src/index.js -c 3 -d _
```

Possible output:
```
cinder_nexus_xenon
```

## License

MIT
