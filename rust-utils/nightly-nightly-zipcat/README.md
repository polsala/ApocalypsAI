# nightly-zipcat

Inspect zip archives from the command line.

## Usage

```sh
nightly-zipcat <zip-file> [--preview N] [--filter <pattern>]
```

- `<zip-file>`: Path to the zip archive.
- `--preview N`: Show first N bytes of each file (default 16).
- `--filter <pattern>`: Only show entries whose names contain the pattern.

## Example

```sh
nightly-zipcat assets.zip --preview 8
```

Outputs:

```
file1.txt: 48 65 6c 6c 6f 20 57 6f
image.png: 89 50 4e 47 0d 0a 1a 0a
```

## Installation

```sh
cargo install --path .
```
