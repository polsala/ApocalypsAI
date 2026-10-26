# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

Welcome, digital janitor! The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-powerful command-line utility designed to help you reclaim your digital space from the insidious accumulation of old, unused files – what we affectionately call "digital dust bunnies".

These forgotten files can clutter your directories, consume precious storage, and generally make your digital life feel a bit... dusty. This tool helps you identify them and decide their fate: a gentle listing, a move to a "digital attic" (quarantine), or a permanent sweep into the void.

## ✨ Features

*   **Scan & Identify**: Recursively scans a specified directory for files older than a configurable age threshold.
*   **List**: Simply lists the identified "dust bunnies" with their size and last modified date.
*   **Quarantine**: Moves old files to a designated "digital attic" folder, keeping them out of sight but retrievable.
*   **Delete**: Permanently removes the files (requires explicit `--force` for safety).
*   **Cross-Platform**: Built with Node.js, it runs wherever Node.js runs.

## 🚀 Installation

1.  **Ensure Node.js is installed**: If you don't have Node.js, download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository** (if not already part of the ApocalypsAI collection):
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-bunny-sweeper
    ```
3.  **Install dependencies** (if any, though this utility aims to be dependency-free):
    ```bash
    npm install
    ```

## 🛠️ Usage

Run the utility using `node src/index.js` followed by the desired options.

```bash
node src/index.js [options]
```

### Options:

*   `--dir <path>`: **(Required)** The directory to scan for digital dust bunnies. Defaults to the current working directory if not specified.
*   `--age <days>`: **(Optional)** Files older than this many days are considered dust bunnies. Must be a positive number. Defaults to `90` days.
*   `--action <list|quarantine|delete>`: **(Optional)** The action to perform:
    *   `list`: (Default) Just list the identified dust bunnies.
    *   `quarantine`: Move them to a specified `--quarantine-dir`.
    *   `delete`: Permanently delete the files. **Requires `--force` for safety.**
*   `--quarantine-dir <path>`: **(Optional)** The directory where files will be moved during a `quarantine` action. Defaults to `./.digital_attic` within the scanned directory.
*   `--force`: **(Optional)** Skips confirmation for the `delete` action. **Use with extreme caution!**
*   `-h`, `--help`: Display help information and exit.

### Examples:

1.  **List all dust bunnies older than 180 days in your Downloads folder:**
    ```bash
    node src/index.js --dir ~/Downloads --age 180 --action list
    ```

2.  **Quarantine all dust bunnies older than 30 days in your current project directory:**
    ```bash
    node src/index.js --dir . --age 30 --action quarantine
    ```

3.  **Move dust bunnies from `/tmp` to a custom digital attic:**
    ```bash
    node src/index.js --dir /tmp --age 7 --action quarantine --quarantine-dir /var/digital_attic_tmp
    ```

4.  **Permanently delete very old temporary files (use with caution!):**
    ```bash
    node src/index.js --dir /var/log/old_temp --age 365 --action delete --force
    ```

## 🧪 Testing

To run the automated tests for this utility:

```bash
npm test
```

The tests use `jest` (installed as a dev dependency) and mock file system operations to ensure deterministic and offline execution without affecting your actual files.

## 🤝 Contributing

Feel free to sweep in with improvements, bug fixes, or new whimsical features! Please ensure your contributions adhere to the project's code style and include relevant tests.
