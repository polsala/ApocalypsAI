# nightly-disk-usage-summary

A small Rust CLI that walks a directory tree and prints a table of the sizes of each immediate sub‑folder, accompanied by a light‑hearted commentary based on the size.

## Features

* Recursively calculates the total size of each sub‑folder.
* Human‑readable output (B, KB, MB, GB).
* A short, whimsical comment for each folder:
  * **> 1 GB** – "This folder is a treasure trove!"
  * **< 1 MB** – "This folder is a barren wasteland!"
  * otherwise – "This folder is moderately populated."
* Works on any platform that supports Rust.

## Installation

```bash
cargo install nightly-disk-usage-summary
```

## Usage

```bash
# Show summary for the current directory
nightly-disk-usage-summary

# Show summary for a specific path
nightly-disk-usage-summary /path/to/dir
```

## Example Output

```
Disk usage summary for: /tmp
Folder                         Size        Commentary
------------------------------------------------------------
subfolder1                     2.00 MB     This folder is moderately populated.
subfolder2                     500 B       This folder is a barren wasteland!
subfolder3                     1.50 GB     This folder is a treasure trove!
```

## Testing

Run the test suite with:

```bash
cargo test
```

The tests create temporary directories and verify that the size calculation and human‑readable formatting work as expected.
