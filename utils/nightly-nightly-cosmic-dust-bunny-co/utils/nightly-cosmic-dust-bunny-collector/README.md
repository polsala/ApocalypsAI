# Nightly Cosmic Dust Bunny Collector

## 🌌🧹 Declutter Your Digital Cosmos! 🧹🌌

The universe is vast, and so are our file systems. Over time, empty directories accumulate like cosmic dust bunnies, taking up mental space and making navigation a chore. The **Nightly Cosmic Dust Bunny Collector** is here to help! This whimsical utility scans a specified directory for these digital voids and, with your permission, tidies them away.

### ✨ Features

*   **Recursive Scanning**: Dives deep into your directory structure to find every last dust bunny.
*   **Preview Mode**: See which directories are empty before committing to deletion.
*   **Safe Deletion**: Only removes truly empty directories.
*   **Whimsical Reporting**: Get a summary of your newly decluttered digital cosmos.

### 🚀 Usage

```bash
python src/collector.py --path /path/to/scan
```

This command will scan `/path/to/scan` and its subdirectories, listing all empty directories found. It will **not** delete anything by default.

To actually delete the empty directories:

```bash
python src/collector.py --path /path/to/scan --delete
```

### 🛠️ Development

The collector is written in Python 3.11 and uses standard library modules.

#### Running Tests

```bash
python -m unittest tests/test_collector.py
```

### 📜 License

This utility is part of the ApocalypsAI project and is licensed under the MIT License.
