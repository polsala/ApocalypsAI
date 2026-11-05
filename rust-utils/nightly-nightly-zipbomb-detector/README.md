# nightly-zipbomb-detector

Detects potential zip bombs by analyzing the compression ratio of zip archives.

## Usage

```sh
nightly-zipbomb-detector <path-to-zip>
```

- If the uncompressed size is more than **100×** the compressed size, the tool prints a warning and exits with code **1**.
- Otherwise it prints `OK` and exits with code **0**.

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
