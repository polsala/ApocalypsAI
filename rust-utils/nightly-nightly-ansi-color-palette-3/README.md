# nightly-ansi-color-palette

A tiny Rust CLI that translates common color names into their ANSI escape codes for terminal text styling.

## Usage

```sh
cargo run --quiet -- <color>
```

Example:

```sh
$ cargo run --quiet -- red
31
```

## Supported colors

- black
- red
- green
- yellow
- blue
- magenta
- cyan
- white
- bright_black
- bright_red
- bright_green
- bright_yellow
- bright_blue
- bright_magenta
- bright_cyan
- bright_white

## Build

```sh
cargo build --release
```

## Test

```sh
cargo test
```
