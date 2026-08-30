# nightly-ramble-tips

A whimsical CLI that spits out a random post‑apocalyptic survival tip. Provide `--seed` for deterministic output, perfect for scripting or testing.

## Usage

```sh
nightly-ramble-tips          # random tip
nightly-ramble-tips --seed 42   # deterministic tip
```

## Installation

```sh
cargo install --path .
```

## Example

```
$ nightly-ramble-tips --seed 42
A well‑maintained flashlight is worth more than gold.
```
