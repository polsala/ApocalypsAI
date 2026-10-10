# Nightly Scavenge Log (nightly-scavenge-log)

A crucial Bash utility for every diligent wasteland scavenger! This tool helps you meticulously log your daily finds, categorize them, and generate a manifest to keep track of your precious resources. No more forgetting where you stashed that last can of irradiated beans!

## Features

*   **Log New Finds:** Quickly record items, their categories, and quantities.
*   **Daily Overview:** See all your scavenged items for the current day.
*   **Manifest Generation:** Create a detailed report for any specific day.
*   **Simple & Robust:** Pure Bash, minimal dependencies, designed for the harsh realities of the post-apocalypse.

## Installation

1.  **Clone the repository (or just this utility):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/bash-utils/nightly-scavenge-log
    ```
2.  **Make the script executable:**
    ```bash
    chmod +x src/scavenge-log.sh
    ```
3.  **Optional: Add to your PATH for easy access:**
    ```bash
    # Example for ~/.bashrc or ~/.zshrc
    echo 'export PATH="$PATH:/path/to/ApocalypsAI/bash-utils/nightly-scavenge-log/src"' >> ~/.bashrc
    source ~/.bashrc
    ```
    (Replace `/path/to/ApocalypsAI/bash-utils/nightly-scavenge-log/src` with the actual path.)

## Usage

The utility stores logs in `~/.apocalypsai_scavenge_logs/`.

### 1. Log a new scavenged item

```bash
scavenge-log.sh add "<item_name>" "<category>" <quantity>
```

*   `<item_name>`: The name of the item (e.g., "Rusty Can", "Mutant Fungus").
*   `<category>`: The category of the item (e.g., "Food", "Components", "Water", "Weapon").
*   `<quantity>`: The number of items found (a positive integer).

**Example:**
```bash
scavenge-log.sh add "Pre-War Comic Book" "Entertainment" 1
scavenge-log.sh add "Scrap Metal" "Components" 15
scavenge-log.sh add "Purified Water" "Water" 3
```

### 2. View today's scavenge log

```bash
scavenge-log.sh view
```

This will display all items logged for the current date.

### 3. Generate a manifest for a specific day

```bash
scavenge-log.sh manifest <YYYY-MM-DD>
```

*   `<YYYY-MM-DD>`: The date for which you want to see the manifest (e.g., `2077-10-23`).

**Example:**
```bash
scavenge-log.sh manifest 2077-10-23
```

## Development & Testing

The utility includes a self-contained test script.

To run tests:
```bash
./tests/test_scavenge-log.sh
```

Tests are deterministic and use a temporary log directory and a mocked date to ensure consistent results.
