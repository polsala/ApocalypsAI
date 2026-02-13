# nightly-entropy-analyzer

Compute the Shannon entropy of a given string.

## Usage

```sh
# Pipe input
echo "your text" | nightly-entropy-analyzer

# Or pass as an argument
nightly-entropy-analyzer "your text"
```

The tool prints the entropy in bits with four decimal places.

## Example

```
$ nightly-entropy-analyzer "abcd"
2.0000
```

## Building

```sh
cargo build --release
```
