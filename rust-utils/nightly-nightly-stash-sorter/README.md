# nightly-stash-sorter

A high-performance command-line utility for the discerning scavenger, written in Rust. This tool helps you organize your precious finds by categorizing them based on keywords and then sorting them for easy access. Whether you're sorting actual survival gear or just your digital downloads, `nightly-stash-sorter` brings order to chaos.

## Features

*   **Fast Categorization**: Quickly assigns items to predefined categories like "Sustenance", "Tools & Tech", "Barter & Bling", and "Mysterious Artifacts".
*   **Customizable Rules**: Define your own categories and keywords using a simple TOML configuration file.
*   **Input Flexibility**: Reads items from standard input or a specified file, one item per line.
*   **Clean Output**: Presents your sorted stash in a clear, categorized format.

## Installation

To install `nightly-stash-sorter`, you'll need Rust and Cargo installed. If you don't have them, visit [rustup.rs](https://rustup.rs/) for instructions.

```bash
cargo install nightly-stash-sorter
```

Alternatively, clone the repository and build from source:

```bash
git clone https://github.com/polsala/ApocalypsAI.git
cd ApocalypsAI/rust-utils/nightly-stash-sorter
cargo build --release
# The executable will be in target/release/nightly-stash-sorter
```

## Usage

Pipe items to the tool:

```bash
echo -e "rusty wrench\ncan of beans\nshiny button\nglowing orb\nbottle of water" | nightly-stash-sorter
```

Read items from a file:

```bash
# items.txt
# rusty wrench
# can of beans
# shiny button
# glowing orb
# bottle of water
nightly-stash-sorter -f items.txt
```

Use a custom rules file:

First, create a `rules.toml` file (example below).

```toml
# rules.toml
[categories.survival_food]
keywords = ["beans", "ration", "canned"]

[categories.medical_supplies]
keywords = ["bandages", "medkit", "antiseptic"]

[categories.rare_finds]
keywords = ["gem", "artifact", "ancient"]
```

Then run the sorter with your custom rules:

```bash
echo -e "canned peaches\nold bandages\nshiny gem" | nightly-stash-sorter -r rules.toml
```

### Command Line Arguments

*   `-f, --file <FILE>`: Path to a file containing items (one per line). If not provided, reads from stdin.
*   `-r, --rules <FILE>`: Path to a TOML file defining custom categories and keywords.
*   `-h, --help`: Prints help information.
*   `-V, --version`: Prints version information.

## Example Output

```
--- Stash Report ---

[Sustenance]
  - Bottle of water
  - Can of beans

[Tools & Tech]
  - Rusty wrench

[Barter & Bling]
  - Shiny button

[Mysterious Artifacts]
  - Glowing orb

[Miscellaneous]
  - (No items)
```

## Development

To run tests:

```bash
cargo test
```

## License

This project is licensed under the MIT License.
