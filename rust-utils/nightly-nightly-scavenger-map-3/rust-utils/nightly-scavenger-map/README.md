# Scavenger Map Generator

A whimsical Rust CLI that creates a tiny ASCII map showing where to find your scavenged items in a post‑apocalyptic world.

## Usage

```sh
cargo run -- <item1> <item2> ...
```

Example:

```sh
cargo run -- water canned-food medkit
```

Outputs something like:

```
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
. . . . . . . . . .
```

(Actual map will have letters representing items.)

## Testing

```sh
cargo test
```
