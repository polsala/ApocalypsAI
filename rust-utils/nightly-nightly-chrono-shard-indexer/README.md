# Nightly Chrono-Shard Indexer

In the fractured timelines of the post-apocalypse, information is often scattered into tiny, ephemeral fragments – "chrono-shards." The `nightly-chrono-shard-indexer` is a robust, high-performance Rust CLI tool designed to help you gather, index, search, and deduplicate these precious textual remnants.

Whether you're sifting through ancient log files, survivor notes, or cryptic data fragments, this tool ensures your vital information is organized and retrievable, even when the fabric of reality is not.

## Features

*   **Index Shards:** Recursively scans a directory for text files, generating a unique hash for each, and storing metadata (path, hash, first line snippet) in a `.chrono_index.json` file.
*   **Search Shards:** Quickly searches the indexed shards for keywords, displaying matching files and their snippets.
*   **Deduplicate Shards:** Identifies and lists (or optionally removes) files with identical content, helping you reclaim precious storage space and reduce data redundancy.
*   **High Performance:** Built with Rust for speed and efficiency, ideal for large collections of small files.

## Installation

To install `nightly-chrono-shard-indexer`, you'll need Rust and Cargo installed.

```bash
# Clone the repository (or navigate to the utility's directory)
# git clone https://github.com/polsala/ApocalypsAI.git
# cd ApocalypsAI/rust-utils/nightly-chrono-shard-indexer

cargo install --path .
```

This will install the `chrono-shard-indexer` binary to your Cargo bin directory, usually `~/.cargo/bin`.

## Usage

```bash
chrono-shard-indexer <COMMAND>
```

### Commands:

*   `index <PATH>`: Indexes all text files in the specified directory and its subdirectories.
    *   `<PATH>`: The directory to scan. Defaults to the current directory if not provided.
    *   `--output <FILE>`: Specify a custom output path for the index file. Defaults to `.chrono_index.json` in the scanned directory.

    Example:
    ```bash
    chrono-shard-indexer index ./my_shards
    chrono-shard-indexer index . --output my_custom_index.json
    ```

*   `search <KEYWORD>`: Searches the index for shards containing the specified keyword.
    *   `<KEYWORD>`: The term to search for.
    *   `--index <FILE>`: Specify the index file to use. Defaults to `.chrono_index.json` in the current directory.

    Example:
    ```bash
    chrono-shard-indexer search "anomaly detected"
    chrono-shard-indexer search "survival guide" --index ./my_shards/.chrono_index.json
    ```

*   `deduplicate`: Finds and lists duplicate shards based on their content hash.
    *   `--index <FILE>`: Specify the index file to use. Defaults to `.chrono_index.json` in the current directory.
    *   `--delete`: **(USE WITH CAUTION!)** Deletes all but one instance of each duplicate file.

    Example:
    ```bash
    chrono-shard-indexer deduplicate
    chrono-shard-indexer deduplicate --index ./my_shards/.chrono_index.json --delete
    ```

## Examples

1.  **Indexing your salvaged data fragments:**
    ```bash
    # Assuming you have a directory 'salvaged_data' with many text files
    chrono-shard-indexer index ./salvaged_data
    # An index file named .chrono_index.json will be created in ./salvaged_data
    ```

2.  **Finding mentions of a specific resource:**
    ```bash
    chrono-shard-indexer search "water purification" --index ./salvaged_data/.chrono_index.json
    ```

3.  **Cleaning up redundant logs:**
    ```bash
    chrono-shard-indexer deduplicate --index ./salvaged_data/.chrono_index.json
    # Review the output, then if confident:
    # chrono-shard-indexer deduplicate --index ./salvaged_data/.chrono_index.json --delete
    ```
