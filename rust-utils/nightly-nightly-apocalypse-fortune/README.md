# Nightly Apocalypse Fortune

A tiny Rust CLI that prints a random post‑apocalypse themed fortune message. Perfect for a quick morale boost in the wasteland.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
nightly-apocalypse-fortune
```

Each run prints one of several whimsical fortunes.

## How it works

The program stores a static list of fortunes and selects one at random using the `rand` crate.
