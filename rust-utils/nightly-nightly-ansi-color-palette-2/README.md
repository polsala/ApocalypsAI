# nightly-ansi-color-palette

**What it does**

`nightly-ansi-color-palette` is a tiny Rust command‑line tool that prints the entire 256‑color ANSI palette. Each cell shows:

* the color index (0‑255)
* the RGB hex code (e.g. `#ff00ff`)
* a colored block using the terminal's true‑color escape sequence

The output is arranged in a 16 × 16 grid, making it easy to pick colors for terminal themes, scripts, or just for fun.

**Installation**

```bash
# Clone the repository (or copy the generated folder) and build
git clone https://github.com/polsala/ApocalypsAI.git
cd utils/rust-utils/nightly-ansi-color-palette
cargo build --release
```

The binary will be at `target/release/nightly-ansi-color-palette`.

**Usage**

```bash
./target/release/nightly-ansi-color-palette
```

You can also pipe the output to `less -R` for paging:

```bash
./target/release/nightly-ansi-color-palette | less -R
```

**Example output (truncated)**

```
  0 #000000 █   1 #800000 █   2 #008000 █   3 #808000 █   4 #000080 █   5 #800080 █   6 #008080 █   7 #c0c0c0 █   8 #808080 █   9 #ff0000 █  10 #00ff00 █  11 #ffff00 █  12 #0000ff █  13 #ff00ff █  14 #00ffff █  15 #ffffff █
 16 #000000 █  17 #00005f █  18 #000087 █  19 #0000af █  20 #0000d7 █  21 #0000ff █  22 #005f00 █  23 #005f5f █  ...
```

**Testing**

Run the test suite with:

```bash
cargo test
```

The tests verify the colour conversion logic for a handful of representative indexes.
