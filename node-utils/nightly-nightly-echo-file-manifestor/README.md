# Nightly Echo File Manifestor

## Summary
This utility helps you manage the 'digital echoes' of files by creating 'ghost files' – empty placeholders that serve as reminders or temporary markers for paths that once existed or are planned. It's a whimsical way to keep track of mental clutter or project structures without the actual file bulk.

## Features
-   **Manifest Ghosts**: Create empty `.ghost` files for specified paths in a designated 'ghost directory'.
-   **Custom Content**: Add a custom message to your ghost files for more context.
-   **List Ghosts**: See all currently manifested ghost files.
-   **Clean Ghosts**: Remove all generated ghost files from the ghost directory.

## Installation
1.  Navigate to the `node-utils/nightly-echo-file-manifestor` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

### Manifesting Ghost Files
Create ghost files for one or more paths. The utility will create a file named `<original_filename>.ghost` in the specified ghost directory.

```bash
node src/index.js manifest <path1> [path2 ...] [--ghost-dir <directory>] [--content <message>]
```

-   `<path1> [path2 ...]`: One or more paths for which to create ghost files. These can be real or imagined paths.
-   `--ghost-dir <directory>`: (Optional) The directory where ghost files will be created. Defaults to `./.ghost_manifest`.
-   `--content <message>`: (Optional) A custom message to include in the ghost file. Defaults to a generic echo message.

**Example:**
```bash
node src/index.js manifest deleted-project/src/main.js deleted-project/README.md --ghost-dir ./my-ghosts --content "Echo of a forgotten file"
```

### Listing Ghost Files
View all ghost files currently residing in the ghost directory.

```bash
node src/index.js list [--ghost-dir <directory>]
```

**Example:**
```bash
node src/index.js list --ghost-dir ./my-ghosts
```

### Cleaning Ghost Files
Remove all `.ghost` files from the specified ghost directory.

```bash
node src/index.js clean [--ghost-dir <directory>]
```

**Example:**
```bash
node src/index.js clean --ghost-dir ./my-ghosts
```

## Development

### Running Tests
```bash
npm test
```
