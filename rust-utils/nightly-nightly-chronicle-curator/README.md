# Nightly Chronicle Curator

A high-performance CLI tool crafted in Rust to help you curate your digital history by organizing files into a chronological, date-based directory structure. Say goodbye to chaotic download folders and hello to a beautifully ordered archive of your digital moments!

## ✨ Features

*   **Chronological Organization**: Automatically sorts files into `YYYY/MM/DD/` directories based on their creation or modification date.
*   **Flexible Source & Destination**: Specify any source directory to scan and any destination for your curated chronicle.
*   **Creation or Modification Time**: Choose whether to use the file's creation timestamp (default) or its last modification timestamp for sorting.
*   **Dry Run Mode**: Preview the organization without making any changes to your files, ensuring peace of mind.
*   **Hidden File Control**: Option to include or exclude hidden files and directories from the curation process.
*   **Blazing Fast**: Built with Rust for optimal performance, even with large collections of files.

## 🚀 Installation

### From Source (Requires Rust Toolchain)

1.  **Install Rust**: If you don't have Rust installed, follow the instructions on [rustup.rs](https://rustup.rs/).
2.  **Clone the repository**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-chronicle-curator
    ```
3.  **Build the utility**:
    ```bash
    cargo build --release
    ```
4.  **Run from target**: The executable will be located at `target/release/nightly-chronicle-curator`. You can add this path to your system's `PATH` for easier access, or move it to a common `bin` directory.

## 💡 Usage

```bash
nightly-chronicle-curator [OPTIONS]
```

### Arguments:

*   `-s, --source <PATH>`: The source directory to scan for files. Defaults to the current directory (`.`).
*   `-d, --destination <PATH>`: The destination directory where organized files will be placed. Defaults to `./chronicle`.
*   `-m, --modified`: Use modification time instead of creation time for organizing files.
*   `-n, --dry-run`: Only show what would be done, without actually moving files.
*   `-a, --all`: Include hidden files and directories in the curation process.

### Examples:

1.  **Organize files in the current directory into `./chronicle` (default behavior, uses creation time):**
    ```bash
    nightly-chronicle-curator
    ```

2.  **Organize files from `~/Downloads` into `~/MyChronicle` using modification time:**
    ```bash
    nightly-chronicle-curator -s ~/Downloads -d ~/MyChronicle -m
    ```

3.  **Perform a dry run to see what would happen without moving anything:**
    ```bash
    nightly-chronicle-curator -s ~/Photos -d ~/PhotoArchive -n
    ```

4.  **Organize files including hidden ones:**
    ```bash
    nightly-chronicle-curator -s ~/Documents -d ~/DocArchive -a
    ```

## 🧪 Testing

To run the integration tests:

```bash
cd rust-utils/nightly-chronicle-curator
cargo test --workspace
```

The tests create temporary directories and dummy files to simulate file system operations, ensuring deterministic and offline validation of the utility's behavior.
