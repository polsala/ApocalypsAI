# Nightly ASCII Art Generator

A whimsical command-line tool that converts text into ASCII art banners using a curated selection of fonts.

## Features
- Convert any text into ASCII art
- Choose from multiple built-in fonts
- Preview all available fonts
- Cross-platform compatibility

## Installation

```bash
# Clone the repository
git clone https://github.com/polsala/ApocalypsAI.git

cd ApocalypsAI/rust-utils/nightly-ascii-art-generator

# Build the project
cargo build --release

# Run the binary
./target/release/nightly-ascii-art-generator --help
```

## Usage

```bash
# Basic usage
./target/release/nightly-ascii-art-generator "Hello World"

# Use a specific font
./target/release/nightly-ascii-art-generator "Hello World" --font slant

# List all available fonts
./target/release/nightly-ascii-art-generator --list-fonts

# Preview all fonts with sample text
./target/release/nightly-ascii-art-generator --preview-all
```

## Supported Fonts
- standard
- slant
- big
- small
- script
- banner

## License
MIT
