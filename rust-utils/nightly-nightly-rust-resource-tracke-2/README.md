# Nightly Rust Resource Tracker

A blazing-fast CLI tool for tracking and managing post-apocalyptic resources with real-time analytics.

## Features

- **Lightning-fast**: Built with Rust for maximum performance
- **Real-time tracking**: Monitor resource levels in real-time
- **Analytics dashboard**: Built-in analytics for resource trends
- **Export capabilities**: Export data to JSON, CSV, or SQLite
- **Interactive CLI**: User-friendly command-line interface

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd nightly-rust-resource-tracker

# Build the project
cargo build --release

# Run the tracker
./target/release/nightly-rust-resource-tracker
```

## Usage

```bash
# Add a new resource
./target/release/nightly-rust-resource-tracker add --name "Water" --quantity 100 --category "Essentials"

# View all resources
./target/release/nightly-rust-resource-tracker list

# Export to JSON
./target/release/nightly-rust-resource-tracker export --format json --output resources.json

# Start interactive mode
./target/release/nightly-rust-resource-tracker interactive
```

## Commands

- `add`: Add a new resource
- `list`: List all resources
- `update`: Update resource quantity
- `remove`: Remove a resource
- `export`: Export data to various formats
- `interactive`: Start interactive mode
- `help`: Show help information

## License

MIT License
