# Nightly Scavenger Manifest Manager

## 📦 Overview

The Nightly Scavenger Manifest Manager is a crucial utility for any discerning post-apocalyptic survivor. It helps you keep track of your precious scavenged goods, ensuring you never lose sight of that last can of beans or that vital piece of scrap metal. Organize, search, and manage your inventory with ease, because in the wasteland, every item counts!

## ✨ Features

*   **Add Items**: Easily log new discoveries with a name, description, quantity, and tags.
*   **List Manifest**: View your entire inventory at a glance.
*   **Search & Filter**: Quickly find items by name or specific tags (e.g., "food", "crafting", "medical").
*   **Remove Items**: Update your manifest when items are used or traded.
*   **Persistent Storage**: Your manifest is saved to a local JSON file, so your hard-earned inventory is never lost, even if the lights go out.

## 🚀 Usage

1.  **Navigate**: Change into the `src` directory:
    ```bash
    cd utils/nightly-scavenger-manifest-manager/src
    ```
2.  **Run**: Execute the script with Python:
    ```bash
    python manifest_manager.py
    ```
3.  **Commands**: Follow the on-screen prompts. Available commands are:
    *   `add`: Add a new item.
    *   `list`: Display all items in the manifest.
    *   `search <query>`: Search items by name or tag.
    *   `remove <item_id>`: Remove an item by its ID.
    *   `save`: Manually save the current manifest (auto-saves on exit).
    *   `load`: Manually load the manifest from file.
    *   `exit`: Save and exit the program.

## 🛠️ Development

The utility is written in Python 3.11 and uses standard library features.

### Running Tests

To run the tests, navigate to the utility's root directory and use `pytest`:

```bash
cd utils/nightly-scavenger-manifest-manager/
python -m pytest tests/
```
