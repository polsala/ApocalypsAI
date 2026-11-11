# Nightly Echo Scrubber

## "Silence the Whispers of Repetition"

In the vast, echoing chambers of data, sometimes the same message reverberates, slightly altered, or perfectly identical. These are the 'temporal echoes' – redundant whispers from the recent past that clutter our perception. The `nightly-echo-scrubber` is a high-performance Rust CLI tool designed to silence these echoes, ensuring clarity and conciseness in your text files and logs.

Whether it's exact duplicates or subtle reverberations (fuzzy matches), this tool helps you clean your data streams, focusing only on the truly unique signals.

## Installation

Ensure you have Rust and Cargo installed. Then, you can install the `nightly-echo-scrubber` directly from source:

```bash
cargo install --path .
```

Or, if published to crates.io (future):

```bash
cargo install nightly-echo-scrubber
```

## Usage

Pipe content to `nightly-echo-scrubber` or specify a file path. By default, it performs exact deduplication.

```bash
# Deduplicate lines from a file (exact match)
nightly-echo-scrubber my_log_file.txt

# Deduplicate lines from stdin (exact match)
cat my_log_file.txt | nightly-echo-scrubber

# Enable fuzzy matching (case-insensitive, whitespace-trimmed)
nightly-echo-scrubber --fuzzy my_log_file.txt

# Enable fuzzy matching with a temporal window of 5 recent unique lines
nightly-echo-scrubber --fuzzy --window 5 my_log_file.txt

# Report detected echoes to stderr instead of just suppressing them
nightly-echo-scrubber --report-echoes my_log_file.txt

# Combine fuzzy matching, window, and reporting
nightly-echo-scrubber --fuzzy --window 10 --report-echoes my_log_file.txt
```

## Options

*   `-f`, `--fuzzy`: Enable fuzzy matching. Lines are considered duplicates if they are identical after being converted to lowercase and having leading/trailing whitespace trimmed. This helps catch 'temporal echoes' that are slightly distorted.
*   `-w <N>`, `--window <N>`: When fuzzy matching is enabled, this sets the size of the 'temporal window' (history buffer) for detecting echoes. Only unique lines within the last `N` processed unique lines are considered for fuzzy comparison. Defaults to `0` (meaning all previously seen unique fuzzy lines are considered).
*   `-r`, `--report-echoes`: Report detected echoes to `stderr`. By default, echoes are silently suppressed.
*   `<FILE>`: The input file to process. If not provided, `nightly-echo-scrubber` reads from `stdin`.
