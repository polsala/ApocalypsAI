# Nightly Digital Dust Sweeper

A whimsical-yet-useful Node.js CLI tool to help you tidy up your digital workspace by finding "digital dust bunnies" – files that haven't been modified in a long, long time. Think of it as a magical broom for your file system, sweeping away the forgotten and the stale.

## 🗑️ What are Digital Dust Bunnies?

In the vast, ever-expanding universe of your file system, some files get created, used once, and then left to gather "digital dust." They sit there, taking up space, cluttering your directories, and generally making your digital life feel a bit... dusty. This tool helps you identify these forgotten relics so you can decide whether to archive them, delete them, or perhaps even rediscover a long-lost treasure!

## ✨ Features

*   **Recursive Scanning**: Traverses directories and their subdirectories to find stale files everywhere.
*   **Age-Based Filtering**: Specify how many days old a file must be to be considered a "dust bunny."
*   **Whimsical Output**: Friendly messages to guide your cleanup efforts.
*   **Cross-Platform**: Works wherever Node.js runs (Windows, macOS, Linux).

## 🚀 Usage

### Prerequisites

Make sure you have Node.js (v14 or higher recommended) installed on your system.

### Running the Sweeper

1.  Navigate to the `nightly-digital-dust-sweeper` directory.
2.  Run the script using `node` and provide the target directory path and the age threshold in days.

```bash
node src/index.js <directory_path> <days_old>
```

**Example:**

To find all files in your current directory (`.`) that haven't been modified in the last 90 days:

```bash
node src/index.js . 90
```

To sweep your `~/Downloads` folder for files older than 30 days:

```bash
node src/index.js ~/Downloads 30
```

### Output

If dust bunnies are found, the tool will list them:

```
Sweeping for digital dust bunnies older than 30 days in: /path/to/my/project

🗑️ Found these digital dust bunnies:
- /path/to/my/project/old_report.pdf
- /path/to/my/project/archive/temp_backup.zip
- /path/to/my/project/src/legacy_module.js

Consider archiving or deleting these 3 files.
```

If your directory is spotless:

```
Sweeping for digital dust bunnies older than 30 days in: /path/to/my/clean/project

✨ No digital dust bunnies found! Your directory is sparkling clean.
```

## 🧪 Development & Testing

The utility includes a comprehensive test suite using `jest`.

### Running Tests

1.  Install `jest` (if not already installed globally or locally):
    ```bash
    npm install jest
    ```
    or
    ```bash
    npm install --save-dev jest
    ```
2.  Run the tests from the utility's root directory:
    ```bash
    npx jest tests/index.test.js
    ```

The tests use mocks for file system operations (`fs.promises`) and `Date.now()` to ensure determinism and avoid actual disk interaction.
