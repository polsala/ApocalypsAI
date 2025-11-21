# Nightly Scavenger Manifest Manager

## 📦 Overview

The `nightly-scavenger-manifest-manager` is a whimsical-yet-useful command-line utility designed to help you keep track of your precious findings in a post-apocalyptic world (or just your cluttered desk). It allows you to add items to your manifest, categorize them, list your entire inventory, and quickly search for specific treasures.

Think of it as your digital ledger for all the shiny bits, canned goods, and mysterious gadgets you've scavenged.

## ✨ Features

*   **Add Items**: Easily add new items with a name, category, and quantity.
*   **List Inventory**: View your entire manifest, neatly organized.
*   **Search**: Quickly find items by name or category using keywords.
*   **Persistent Storage**: Your manifest is saved to a `manifest.json` file, so your findings are safe even after a system reboot (or a zombie attack).

## 🚀 Installation & Usage

This utility is written in Python 3.11 and requires no external dependencies beyond the standard library.

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-scavenger-manifest-manager/src
    ```

2.  **Run the utility**:

    *   **Add an item**:
        ```bash
        python manifest_manager.py add "Rusty Spanner" "Tools" 1
        python manifest_manager.py add "Canned Beans" "Food" 5
        python manifest_manager.py add "Water Bottle (empty)" "Containers" 2
        ```

    *   **List all items**:
        ```bash
        python manifest_manager.py list
        ```

    *   **Search for items**:
        ```bash
        python manifest_manager.py search "beans"
        python manifest_manager.py search "tools"
        ```

## 📂 File Structure

```
nightly-scavenger-manifest-manager/
├── README.md                 # This file
├── src/
│   └── manifest_manager.py   # The main utility script
└── tests/
    └── test_manifest_manager.py # Automated tests for the utility
```
