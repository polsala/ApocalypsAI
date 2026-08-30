# nightly-digital-dust-bunny-sweeper

A whimsical-yet-useful Node.js CLI tool that helps identify and list old, unused files in a directory, categorizing them as "digital dust bunnies" for cleanup. Keep your project directories sparkling clean and free from forgotten relics!

## ✨ Features

- **Recursive Scanning**: Traverses directories to find files everywhere.
- **Age-Based Categorization**: Files are labeled as "Digital Dust Bunny" (90-179 days old), "Forgotten Scroll" (180-364 days old), or "Ancient Relic" (365+ days old).
- **Configurable Age Threshold**: Specify how old a file needs to be to be considered a "dust bunny".
- **Cross-Platform**: Runs wherever Node.js runs.

## 🚀 Usage

### Prerequisites

- Node.js (v14 or higher recommended)

### Installation

This is a standalone utility. Simply clone the repository or copy the `src/dust-bunny-sweeper.js` into your project or a dedicated utilities folder.

```bash
# Assuming you are in the root of the ApocalypsAI repository
cd node-utils/nightly-digital-dust-bunny-sweeper
```

### Running the Sweeper

Execute the script directly using Node.js.

```bash
node src/dust-bunny-sweeper.js [target_directory] [minimum_age_in_days]
```

- `target_directory` (optional): The path to the directory you want to scan. Defaults to the current directory (`.`).
- `minimum_age_in_days` (optional): The minimum age (in days) for a file to be considered a "digital dust bunny". Defaults to `90` days.

#### Examples:

Scan the current directory for files older than 90 days:
```bash
node src/dust-bunny-sweeper.js
```

Scan the `my-old-project` directory for files older than 180 days:
```bash
node src/dust-bunny-sweeper.js my-old-project 180
```

Scan the `/var/log` directory for files older than 365 days:
```bash
node src/dust-bunny-sweeper.js /var/log 365
```

## 🧪 Tests

To run the tests, navigate to the utility's directory and execute the test file:

```bash
cd node-utils/nightly-digital-dust-bunny-sweeper
node tests/test-dust-bunny-sweeper.js
```

The tests use Node.js's built-in `assert` module and mock the file system (`fs`) operations to ensure deterministic and offline execution.
