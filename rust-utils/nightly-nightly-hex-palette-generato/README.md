# nightly-hex-palette-generator

Generate a harmonious palette of hex colors based on a single input color.

## Overview

`nightly-hex-palette-generator` is a tiny CLI tool written in Rust that takes a base hex color (e.g., `#3498db`) and produces a palette of complementary colors by rotating the hue in HSL space. The number of colors can be specified; default is 5.

## Installation

```sh
cargo install --path .
```

## Usage

```sh
nightly-hex-palette-generator #3498db 7
```

Outputs 7 hex colors, one per line.
