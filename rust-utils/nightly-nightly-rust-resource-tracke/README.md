# Nightly Rust Resource Tracker

A high-performance CLI tool for tracking and managing post-apocalyptic resources with real-time updates and inventory management.

## Features

- **Lightning-fast**: Built with Rust for maximum performance
- **Real-time tracking**: Monitor resource levels in real-time
- **Inventory management**: Track supplies, weapons, and survival gear
- **Data persistence**: SQLite-backed storage with automatic backups
- **Export capabilities**: Export data to JSON, CSV, and YAML formats
- **Interactive CLI**: User-friendly command-line interface

## Installation

### From Crates.io
```bash
cargo install nightly-rust-resource-tracker
```

### From Source
```bash
git clone https://github.com/polsala/ApocalypsAI
cd utils/nightly-rust-resource-tracker
cargo build --release
```

## Usage

### Basic Commands
```bash
# Initialize a new resource database
resource-tracker init

# Add a new resource
resource-tracker add --name "Water Purification Tablets" --quantity 50 --category supplies

# View all resources
resource-tracker list

# Update resource quantity
resource-tracker update --name "Water Purification Tablets" --quantity 45

# Export to JSON
resource-tracker export --format json --output resources.json
```

### Advanced Features
```bash
# Set resource expiration date
resource-tracker add --name "Canned Food" --quantity 20 --category food --expires 2025-06-01

# Check for expired items
resource-tracker check-expired

# Generate survival report
resource-tracker report --days 30

# Backup database
resource-tracker backup --path /backup/resources.db
```

## Configuration

Create a `config.toml` file in your home directory:

```toml
[database]
path = "~/.config/resource-tracker/resources.db"
backup_interval = 3600  # seconds

[ui]
color = true
refresh_rate = 5  # seconds

[alerts]
low_threshold = 5
expiring_threshold = 7  # days
```

## License

MIT License - see LICENSE file for details.
