# Nightly Void Whisper Decoder

## Summary
`nightly-void-whisper-decoder` is a whimsical-yet-useful Rust CLI tool designed to bring a semblance of order to garbled or cryptic messages, often encountered in the post-apocalyptic digital wasteland. It applies a series of heuristic 'decoding' rules, including noise removal, simple character interpretation, and keyword highlighting, to make 'void whispers' more coherent and actionable.

While it won't crack advanced ciphers, it's perfect for sifting through static-laden transmissions or fragmented data logs to extract potential meaning.

## Features
-   **Noise Removal**: Strips common digital 'static' patterns like `[STATIC]`, `_VOID_`, `///`, `---`, `...`, `~`.
-   **Character Interpretation**: Applies a fixed, whimsical character substitution to make certain common 'cryptic' letters resemble more standard English characters (e.g., 'X' -> 'E', 'Z' -> 'S').
-   **Keyword Highlighting**: Identifies and highlights crucial survival-related keywords (e.g., "WATER", "FOOD", "DANGER") to draw immediate attention.
-   **Frequency Analysis**: Optionally provides a character frequency breakdown of the *decoded* message, offering hints for further manual interpretation.

## Usage

### Build
To build the utility, navigate to its directory and run:
```bash
cargo build --release
```
The executable will be located at `target/release/void-whisper-decoder`.

### Run

**From a file:**
```bash
./target/release/void-whisper-decoder --file path/to/cryptic_message.txt --interpret --highlight-keywords --frequency-analysis
```

**From standard input:**
```bash
echo "[STATIC] XQZJ KWWV. Find WATER and food. DANGER ahead. ///" | ./target/release/void-whisper-decoder -i -k -f
```

### Arguments
-   `-f`, `--file <FILE>`: Input file to decode. If not provided, reads from stdin.
-   `-i`, `--interpret`: Apply simple character interpretation (whimsical substitution).
-   `-k`, `--highlight-keywords`: Highlight known survival keywords.
-   `-a`, `--frequency-analysis`: Show character frequency analysis of the decoded message.

## Examples

**Basic noise removal and interpretation:**
```bash
echo "[STATIC] XQZJ KWWV. ///" | ./target/release/void-whisper-decoder -i
# Output: EAS I CCUU.
```

**Highlighting keywords:**
```bash
echo "Find water and food. DANGER ahead." | ./target/release/void-whisper-decoder -k
# Output: Find [!water] and [!food]. [!DANGER] ahead.
```

**Full decoding with frequency analysis:**
```bash
echo "~[STATIC] XQZJ KWWV. Find WATER and food. DANGER ahead. --- ..." | ./target/release/void-whisper-decoder -i -k -a
# Output:
# EAS I CCUU. Find [!WATER] and [!food]. [!DANGER] ahead.
# --- Frequency Analysis ---
# A: 4
# D: 1
# E: 3
# F: 1
# G: 1
# H: 1
# I: 1
# N: 2
# O: 2
# R: 2
# S: 1
# T: 2
# U: 2
# W: 1
```

## Tests
To run the automated tests, execute:
```bash
cargo test
```
