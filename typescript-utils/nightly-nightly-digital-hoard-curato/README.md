# Nightly Digital Hoard Curator

## Overview

In the desolate digital wasteland, every byte is precious. The `nightly-digital-hoard-curator` is your trusty companion for organizing your scavenged digital assets. This CLI tool allows you to categorize your files, URLs, and text snippets by 'scarcity' (Common, Uncommon, Rare, Legendary) and 'utility' (Essential, Useful, Archive, Ephemeral). Get a clear overview of your digital hoard and generate curation reports to help you decide what to backup, what to review, and what to let drift into the void.

## Features

*   **Categorize Digital Assets**: Assign scarcity and utility ratings to your digital items.
*   **Persistent Storage**: Your hoard is saved locally in a JSON file.
*   **Curation Reports**: Get actionable suggestions based on your item's ratings.
*   **Simple CLI**: Easy to use command-line interface.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v14 or higher) and npm/yarn installed.
2.  **Navigate**: Change into the `nightly-digital-hoard-curator` directory.
3.  **Install Dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
4.  **Build**: Compile the TypeScript code:
    ```bash
    npm run build
    # or yarn build
    ```

## Usage

Run the utility using `node dist/index.js` or set up an alias.

### Commands:

*   `add <name> <type> <pathOrContent> <scarcity> <utility>`: Adds a new digital item to your hoard.
    *   `name`: A descriptive name for the item (e.g., "Old World Map").
    *   `type`: `file`, `url`, or `text`.
    *   `pathOrContent`: File path, URL, or the text content itself.
    *   `scarcity`: `common`, `uncommon`, `rare`, `legendary`.
    *   `utility`: `essential`, `useful`, `archive`, `ephemeral`.

    Example:
    ```bash
    node dist/index.js add "Ancient Survival Guide" file "/docs/survival.pdf" legendary essential
    node dist/index.js add "Wasteland Water Source" url "https://example.com/water-map" rare useful
    node dist/index.js add "Scavenged Note" text "Found a stash near Sector 7." common ephemeral
    ```

*   `list`: Lists all items in your digital hoard.

    Example:
    ```bash
    node dist/index.js list
    ```

*   `report`: Generates a curation report with suggestions.

    Example:
    ```bash
    node dist/index.js report
    ```

*   `delete <id>`: Deletes an item by its unique ID.

    Example:
    ```bash
    node dist/index.js delete 123e4567-e89b-12d3-a456-426614174000
    ```

## Development

To run tests:

```bash
npm test
# or yarn test
```
