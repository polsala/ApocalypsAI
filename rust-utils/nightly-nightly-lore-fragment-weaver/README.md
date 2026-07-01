# Nightly Lore Fragment Weaver

A high-performance CLI tool crafted in Rust to help the ApocalypsAI community organize and consolidate fragmented textual data, or 'lore fragments', from various sources. Whether you're piecing together ancient prophecies, combining research notes, or just merging log files, this tool ensures each fragment's origin is clearly marked in the woven output.

## Features

*   **Fragment Consolidation**: Combines content from multiple input text files into a single output.
*   **Origin Tracking**: Automatically inserts a header and footer for each fragment, indicating its source filename.
*   **Flexible Output**: Write the woven lore to a specified output file or directly to standard output.
*   **Performance**: Built with Rust for speed and efficiency, ideal for processing large numbers of files or substantial content.

## Installation

To install `lore-weaver`, you need to have Rust and Cargo installed. If you don't, visit [rustup.rs](https://rustup.rs/) for instructions.

1.  Clone the ApocalypsAI repository:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/rust-utils/nightly-lore-fragment-weaver
    ```
2.  Build the utility using Cargo:
    ```bash
    cargo build --release
    ```
3.  The executable will be located at `target/release/lore-weaver`.
    You can add it to your system's PATH for easier access:
    ```bash
    sudo cp target/release/lore-weaver /usr/local/bin/
    ```

## Usage

```bash
lore-weaver -i <FILE1> -i <FILE2> ... [-o <OUTPUT_FILE>]
```

### Arguments:

*   `-i`, `--input <FILE>`: Specify one or more input text files (e.g., `fragment1.txt`). This argument can be provided multiple times.
*   `-o`, `--output <FILE>`: (Optional) Specify the path to the output file where the woven lore will be saved. If omitted, the output will be printed to `stdout`.

### Examples:

1.  **Weave two fragments into a new file:**
    ```bash
    echo "The ancient text spoke of a great cataclysm." > fragment1.txt
    echo "Only the chosen few would survive." > fragment2.txt
    lore-weaver -i fragment1.txt -i fragment2.txt -o woven_story.txt
    cat woven_story.txt
    ```
    *Expected `woven_story.txt` content:*
    ```
    --- LORE FRAGMENT FROM: fragment1.txt ---

    The ancient text spoke of a great cataclysm.

    --- END FRAGMENT ---

    --- LORE FRAGMENT FROM: fragment2.txt ---

    Only the chosen few would survive.

    --- END FRAGMENT ---
    ```

2.  **Weave multiple fragments and print to console:**
    ```bash
    echo "A new dawn approaches." > fragment3.txt
    lore-weaver -i fragment1.txt -i fragment2.txt -i fragment3.txt
    ```
    *Output will be printed to your terminal.*

3.  **Handle an empty fragment:**
    ```bash
    touch empty_fragment.txt
    lore-weaver -i fragment1.txt -i empty_fragment.txt -o combined.txt
    cat combined.txt
    ```
    *The empty fragment will be included with its header/footer, but no content.*

## Development

To run tests:

```bash
cargo test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
