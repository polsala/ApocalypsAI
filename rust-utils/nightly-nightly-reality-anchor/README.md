# Nightly Reality Anchor

In the ever-shifting realities of the post-apocalypse, sometimes you just need to know if a file is still... *itself*. The `nightly-reality-anchor` is a blazing-fast Rust CLI utility that calculates and verifies a stable SHA256 'reality anchor' for your crucial files. Detect temporal drift, data corruption, or mischievous reality-benders with a single command!

## Features

*   **Anchor Files**: Calculate and store a SHA256 hash (the 'reality anchor') for any file.
*   **Verify Stability**: Check if a file's current state matches its stored reality anchor.
*   **Quick Check**: Get a file's current hash without storing or verifying.
*   **High Performance**: Written in Rust for speed and reliability.

## Installation

To build and install from source, you'll need Rust and Cargo installed.

```bash
cargo install --path .
```

This will install the `nightly-reality-anchor` executable to your Cargo bin directory.

## Usage

### 1. Anchor a file

This command calculates the SHA256 hash of `my_important_document.txt` and stores it in a new file named `my_important_document.txt.anchor` in the same directory.

```bash
nightly-reality-anchor anchor my_important_document.txt
```

Output:
```
Reality anchor created for "my_important_document.txt": <SHA256_HASH>
```

### 2. Verify a file's reality

This command compares the current SHA256 hash of `my_important_document.txt` with its stored anchor. It will report success or detect 'temporal drift' if the file has changed.

```bash
nightly-reality-anchor verify my_important_document.txt
```

Output (stable):
```
Reality check PASSED for "my_important_document.txt". Anchor is stable.
```

Output (drift detected):
```
Reality check FAILED for "my_important_document.txt". Temporal drift detected!
  Stored anchor: <OLD_SHA256_HASH>
  Current reality: <NEW_SHA256_HASH>
```

### 3. Check a file's current anchor

This command calculates and prints the current SHA256 hash of the file without interacting with any stored `.anchor` files.

```bash
nightly-reality-anchor check my_important_document.txt
```

Output:
```
Current reality anchor for "my_important_document.txt": <SHA256_HASH>
```

## Development

To run tests:

```bash
cargo test
```
