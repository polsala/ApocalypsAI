# Nightly Chrono-Shard Sorter

A `rust-utils` CLI tool for organizing your digital 'chrono-shards' (files) into neatly arranged 'temporal vaults' (directories) based on their last modification timestamps. Perfect for archiving logs, backups, or just tidying up a chaotic data hoard in the post-apocalyptic digital landscape.

## Features

*   **Timestamp-based Sorting**: Organizes files into `YYYY/MM/DD` directory structures.
*   **Move or Copy**: Choose to move files from the source or create copies, leaving originals intact.
*   **Conflict Resolution**: Automatically renames files with a timestamp suffix if a name collision occurs in the destination.
*   **High Performance**: Built with Rust for speed and reliability.

## Installation

Ensure you have Rust and Cargo installed. If not, follow the instructions at [rustup.rs](https://rustup.rs/).

```bash
cargo install nightly-chrono-shard-sorter
```

Alternatively, clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-chrono-shard-sorter
cargo build --release
# The executable will be in target/release/nightly-chrono-shard-sorter
```

## Usage

```bash
nightly-chrono-shard-sorter --help
```

### Basic Sorting (Move files)

To move all files from `~/my_data_shards` into a new temporal archive in `~/temporal_vault`:

```bash
nightly-chrono-shard-sorter --source ~/my_data_shards --destination ~/temporal_vault
```

### Copying Files

To copy files instead of moving them:

```bash
nightly-chrono-shard-sorter --source ~/my_data_shards --destination ~/temporal_vault --copy
```

### Example

If `~/my_data_shards` contains:

```
~/my_data_shards/
├── logfile_2023-01-15.txt (modified 2023-01-15 10:00:00)
├── report.pdf (modified 2023-03-20 14:30:00)
└── old_note.md (modified 2022-11-05 08:15:00)
```

After running the command, `~/temporal_vault` might look like this:

```
~/temporal_vault/
├── 2022/
│   └── 11/
│       └── 05/
│           └── old_note.md
├── 2023/
│   ├── 01/
│   │   └── 15/
│   │       └── logfile_2023-01-15.txt
│   └── 03/
│       └── 20/
│           └── report.pdf
```

If a file named `report.pdf` already existed in `~/temporal_vault/2023/03/20/`, the new file would be renamed, e.g., `report_1679322600.pdf` (where `1679322600` is the Unix timestamp of its modification date).
