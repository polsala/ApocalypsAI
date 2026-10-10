# Nightly Whisper Archive

A whimsical utility to capture and organize your fleeting digital whispers – those small thoughts, links, code snippets, or ideas that often get lost in the digital ether. Give your whispers a permanent home, tag them for easy retrieval, and search through your personal archive.

## Features

*   **Capture Whispers**: Quickly add new thoughts or snippets.
*   **Tagging**: Organize whispers with multiple tags for better categorization.
*   **Listing**: View all whispers or filter them by specific tags.
*   **Searching**: Find whispers by content or tags using keywords.
*   **Retrieval**: Look up a specific whisper by its unique ID.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation

1.  **Prerequisites**: Ensure you have Node.js (v16 or higher) and npm installed.
2.  **Clone the repository**: If you haven't already, clone the ApocalypsAI repository and navigate to this utility's directory.
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-whisper-archive
    ```
3.  **Install dependencies and build**:
    ```bash
    npm install
    npm run build
    ```
4.  **Make it executable (optional, for global access)**:
    You can link the utility globally or add its `dist` directory to your PATH.
    ```bash
    npm link # This will create a symlink in your global node_modules/bin
    ```
    Now you can run `nightly-whisper-archive` from anywhere.

## Usage

The `nightly-whisper-archive` utility stores your whispers in a JSON file named `.nightly-whisper-archive.json` in your user's home directory.

### Commands

#### 1. Add a new whisper

```bash
nightly-whisper-archive add "My fleeting thought or a useful link: https://example.com" --tags idea,web,dev
```
*   The content should be enclosed in double quotes (`"`) or single quotes (`'`).
*   Tags are optional and should be comma-separated after `--tags`.

#### 2. List whispers

List all whispers, ordered by most recent first:
```bash
nightly-whisper-archive list
```

List whispers filtered by a specific tag:
```bash
nightly-whisper-archive list --tags dev
```

#### 3. Search whispers

Search for whispers containing a specific keyword in their content or tags:
```bash
nightly-whisper-archive search "project idea"
```
*   The search query should be enclosed in double quotes (`"`) or single quotes (`'`).
*   Search is case-insensitive.

#### 4. Show a specific whisper by ID

Retrieve and display the full details of a whisper using its unique ID:
```bash
nightly-whisper-archive show <whisper-id>
```
Replace `<whisper-id>` with the actual ID of the whisper (e.g., `mock-uuid-123`).

## Development

To run tests:
```bash
npm test
```

To rebuild the TypeScript code:
```bash
npm run build
```
