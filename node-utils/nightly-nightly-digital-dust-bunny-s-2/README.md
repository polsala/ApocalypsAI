# Nightly Digital Dust Bunny Sweeper

Sweeps away old, unused files into a 'Digital Compost Bin' for a tidier digital existence.

## 🧹 What it Does

The `Nightly Digital Dust Bunny Sweeper` is a whimsical yet practical utility designed to help you declutter your digital workspace. It scans a specified directory for files that haven't been modified in a configurable number of days (your "digital dust bunnies") and moves them into a special `.digital_compost_bin` quarantine directory. This gives you a chance to review them before permanent deletion, ensuring your important files are safe while keeping your directories sparkling clean.

## ✨ Features

*   **Age-based Sweeping**: Identifies files older than a specified number of days.
*   **Digital Compost Bin**: Moves old files to a dedicated quarantine directory instead of immediate deletion.
*   **Dry Run Mode**: Simulate the sweep to see what would be moved without actually touching your files.
*   **Configurable Paths & Age**: Easily specify the target directory and the age threshold.
*   **Cross-Platform**: Built with Node.js, it runs on Windows, macOS, and Linux.

## 🚀 Installation

1.  **Navigate to the utility directory**:
    ```bash
    cd node-utils/nightly-digital-dust-bunny-sweeper
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```

## 💡 Usage

Run the utility from the command line:

```bash
node src/index.js [options]
```

### Options:

*   `--path <directory>`: The directory to sweep for digital dust bunnies. Defaults to the current directory (`.`).
*   `--age <days>`: Files older than this many days will be considered dust bunnies and swept. Defaults to `90` days.
*   `--dry-run`: Simulate the sweep without moving any files. Useful for previewing changes.
*   `--quarantine-dir <name>`: The name of the directory where old files will be moved. Defaults to `.digital_compost_bin`. This directory will be created inside the `--path`.
*   `--help`, `-h`: Show the help message.

### Examples:

1.  **Sweep the current directory for files older than 60 days (dry run):**
    ```bash
    npm start -- --path . --age 60 --dry-run
    ```

2.  **Move files older than 180 days from your `~/Downloads` folder to a custom compost bin:**
    ```bash
    npm start -- --path ~/Downloads --age 180 --quarantine-dir my_old_downloads
    ```
    *(Note: `~` might need to be expanded to your full home path depending on your shell and Node.js version. For best compatibility, use absolute paths like `/home/user/Downloads` or `C:\Users\User\Downloads`)*

3.  **Perform a default sweep (90 days, current directory, actual move):**
    ```bash
    npm start
    ```

## 🧪 Tests

To run the automated tests:

```bash
npm test
```

The tests use Jest and mock the file system operations to ensure they are deterministic and do not affect your actual files.

## 📜 License

This project is licensed under the MIT License.
