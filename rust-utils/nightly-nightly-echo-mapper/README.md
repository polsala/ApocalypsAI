# Nightly Echo Mapper

A high-performance CLI tool to calculate echo distances to obstacles on a text-based map, aiding navigation in low-visibility scenarios. Imagine you're in a pitch-black cave; this tool helps you 'ping' your surroundings and understand how far the nearest wall is in each cardinal direction.

## Features

*   Parses simple text-based maps.
*   Identifies a starting point (`S`).
*   Calculates echo distances (steps to the nearest obstacle `#` or map boundary) in North, South, East, and West directions.
*   Fast and efficient, built with Rust.

## Usage

Compile and run the `nightly-echo-mapper` executable. It expects the map to be provided via standard input.

### Input Format

The map should be a series of lines, where:

*   `#` represents an obstacle (wall).
*   `.` represents open space.
*   `S` represents your starting position (there should be exactly one `S`).

### Example Input

```
#####
#S..#
#.#.#
#...#
#####
```

### Example Output

For the above input, if `S` is at (1,1):

```
Echo Distances:
North: 1
South: 2
East: 2
West: 1
```

## Build Instructions

To build this utility, you need Rust installed. If you don't have Rust, you can install it via `rustup`:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
```

Once Rust is installed, navigate to the `nightly-echo-mapper` directory and run:

```bash
cargo build --release
```

The executable will be located at `target/release/nightly-echo-mapper`.

## How to Run

You can pipe a map file into the utility:

```bash
cat map.txt | target/release/nightly-echo-mapper
```

Or type the map directly and press `Ctrl+D` (Unix/Linux) or `Ctrl+Z` then `Enter` (Windows) to signal end-of-input:

```bash
target/release/nightly-echo-mapper
#####
#S..#
#.#.#
#...#
#####
<Ctrl+D>
```
