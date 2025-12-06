# Nightly Resource Hoard Manager

## Overview

The `nightly-resource-hoard-manager` is a crucial tool for any survivor looking to keep tabs on their precious supplies in a world gone wild. Whether it's canned beans, purified water, or spare parts for your trusty wasteland buggy, this utility helps you log, track, and manage your inventory with ease. It even warns you about items nearing their expiry date, ensuring no valuable resource goes to waste.

## Features

*   **Add Resources**: Easily add new items to your hoard with a name, quantity, and optional expiry date.
*   **Remove Resources**: Decrement or completely remove items as they are consumed or lost.
*   **List Hoard**: Get a comprehensive overview of all your current resources.
*   **Check Expiries**: Identify items that are nearing their expiry date, allowing you to prioritize their use.

## Usage

This utility operates via the command line. All data is stored in a `hoard.json` file in the same directory where the script is run.

### Prerequisites

*   Python 3.6+

### Commands

To run the manager, navigate to the `src` directory and execute `python manager.py <command> [arguments]`.

*   **Add an item:**
    ```bash
    python manager.py add "Canned Beans" 10 2025-12-31
    python manager.py add "Water Purifier Tablets" 50
    ```
    _Note: Expiry date is optional and should be in YYYY-MM-DD format._

*   **Remove an item:**
    ```bash
    python manager.py remove "Canned Beans" 2
    ```
    _This will reduce the quantity of "Canned Beans" by 2. If the quantity drops to 0 or below, the item is removed._

*   **List all items:**
    ```bash
    python manager.py list
    ```

*   **Check for expiring items (within the next 30 days):**
    ```bash
    python manager.py check-expiry
    ```

## Example Workflow

1.  **Initialize your hoard (first run):**
    ```bash
    python manager.py add "MRE Rations" 5 2026-06-15
    python manager.py add "First Aid Kit" 1
    ```
2.  **Check your inventory:**
    ```bash
    python manager.py list
    ```
3.  **Consume some rations:**
    ```bash
    python manager.py remove "MRE Rations" 1
    ```
4.  **See what's expiring soon (e.g., a month later):**
    ```bash
    python manager.py check-expiry
    ```

## Development

To run tests, navigate to the `tests` directory and execute `python -m unittest test_manager.py`.
