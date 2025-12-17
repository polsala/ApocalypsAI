# Nightly Cipher Canvas

A whimsical CLI tool that encrypts text into ASCII art ciphers using multiple algorithms. Perfect for creating mysterious messages that are both secure and visually entertaining!

## Features

- Encrypt text using Caesar, Atbash, or Vigenère ciphers
- Display encrypted text as ASCII art banners
- Save encrypted messages to files
- Whimsical error messages and Easter eggs

## Installation

### Prerequisites
- Rust 1.70+ and Cargo

### Build from Source
```bash
# Clone the repository
git clone <repo-url>
cd <repo-url>

# Navigate to the utility directory
cd rust-utils/nightly-cipher-canvas

# Build the project
cargo build --release

# Run the CLI
cargo run --release --
```

## Usage

### Basic Encryption
```bash
# Encrypt with Caesar cipher (shift 3)
cargo run --release -- -t "Hello World" -c caesar -s 3

# Encrypt with Atbash cipher
cargo run --release -- -t "Hello World" -c atbash

# Encrypt with Vigenère cipher
cargo run --release -- -t "Hello World" -c vigenere -k "KEY"
```

### ASCII Art Display
```bash
# Display encrypted text as ASCII art
cargo run --release -- -t "Hello World" -c caesar -s 3 -a

# Save encrypted message to file
cargo run --release -- -t "Hello World" -c caesar -s 3 -o encrypted.txt
```

### Help
```bash
# Show help
cargo run --release -- --help
```

## Command Line Options

- `-t, --text`: Text to encrypt (required)
- `-c, --cipher`: Cipher type (caesar, atbash, vigenere)
- `-s, --shift`: Caesar cipher shift (default: 3)
- `-k, --key`: Vigenère cipher key (required for vigenere)
- `-a, --ascii`: Display as ASCII art banner
- `-o, --output`: Output file path
- `-h, --help`: Show help

## Examples

### Caesar Cipher with ASCII Art
```bash
cargo run --release -- -t "ApocalypsAI" -c caesar -s 5 -a
```

### Vigenère Cipher with File Output
```bash
cargo run --release -- -t "Secret Message" -c vigenere -k "RUST" -o secret.txt
```

### Atbash Cipher
```bash
cargo run --release -- -t "Hello" -c atbash -a
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite: `cargo test`
6. Submit a pull request

## Testing

Run the test suite:
```bash
cargo test
```

Run with coverage (if available):
```bash
cargo tarpaulin --out Html
```

## Security Notes

- This tool is for entertainment and educational purposes
- Do not use for actual cryptographic security
- All ciphers are classical and easily breakable with modern techniques

## Whimsical Features

- Easter egg: Try encrypting "42" with Caesar cipher
- Whimsical error messages for invalid inputs
- ASCII art banners for that extra dramatic flair

---

*May your messages be mysterious and your ASCII art be majestic!*
