# Nightly Digital Dust Composter

A whimsical-yet-useful Rust CLI tool for tidying up your digital garden by identifying and 'composting' (deleting) old, unused files, affectionately known as 'digital dust bunnies'.

## Features

*   **Scan Directories**: Recursively scans specified directories for files based on their last modification time.
*   **Age Categorization**: Classifies 'digital dust bunnies' into whimsical categories:
    *   **Fresh Sprouts**: Modified within the last 7 days.
    *   **Wilting Leaves**: Modified between 7 and 30 days ago.
    *   **Ancient Compost**: Modified between 30 and 90 days ago.
    *   **Petrified Relics**: Modified more than 90 days ago.
*   **Size Reporting**: Provides total size for each category and individual file sizes.
*   **Composting (Deletion)**: Optionally deletes identified files.
*   **Whimsical Output**: Presents findings with a touch of apocalyptic charm.

## Installation

To build and install the `nightly-digital-dust-composter`:

1.  Ensure you have Rust and Cargo installed. If not, follow the instructions at [rust-lang.org](https://www.rust-lang.org/tools/install).
2.  Navigate to the `nightly-digital-dust-composter` directory.
3.  Run `cargo build --release` to compile the optimized executable.
4.  The executable will be located at `target/release/nightly-digital-dust-composter`.

## Usage

```bash
nightly-digital-dust-composter [OPTIONS] <PATH>
```

### Arguments

*   `<PATH>`: The directory to scan for digital dust bunnies.

### Options

*   `-a, --age <DAYS>`: Minimum age in days for a file to be considered a 'dust bunny'. Files older than this will be considered. Default is 30 days.
*   `-d, --delete`: Actually delete the identified files. **Use with caution!** By default, the tool only lists files.
*   `-v, --verbose`: Show individual files in each category.
*   `-h, --help`: Print help information.

## Examples

Scan your downloads folder for files older than 60 days, without deleting:

```bash
nightly-digital-dust-composter -a 60 ~/Downloads
```

Scan your temporary folder for files older than 30 days and delete them, showing verbose output:

```bash
nightly-digital-dust-composter -a 30 -d -v /tmp
```
