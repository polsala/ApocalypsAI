# nightly-hexapoc-namer

A tiny Rust CLI that turns a hex colour code into an apocalypse‑themed name.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
hexapoc-namer #ff4500
# => "blazing ember"
```

## How it works

The tool parses the RGB values, computes two simple hashes and selects an adjective and a noun from predefined lists.
