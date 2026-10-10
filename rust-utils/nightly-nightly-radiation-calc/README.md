# Nightly Radiation Calc

A tiny Rust CLI tool that computes the total radiation dose (in millisieverts) given an intensity (mSv/h) and exposure duration (hours). It warns when the dose exceeds the commonly referenced safe limit of 100 mSv.

## Usage

```sh
cargo run -- <intensity> <hours>
```

Example:

```sh
cargo run -- 0.5 48
# => Total dose: 24.00 mSv (safe)
```

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
