# Nightly Digital Dust Bunny Sweeper

Sweeps old, unused files into a designated "Digital Dust Bunny Sanctuary" for whimsical digital decluttering. This utility helps you tidy up your digital space by identifying files that haven't been modified in a specified number of days and moving them to a safe, separate location, rather than deleting them outright. It also cleans up any directories that become empty as a result of the sweeping.

## Features

*   **Whimsical Decluttering**: Don't just delete, *sweep* your digital dust bunnies!
*   **Safe Archiving**: Files are moved, not deleted, giving you a chance to review them later.
*   **Age-Based Filtering**: Define how old a file must be to be considered a "dust bunny."
*   **Empty Directory Cleanup**: Automatically removes directories that become empty after files are swept.
*   **Cross-Platform**: Built with Node.js, it runs wherever Node.js runs.

## Installation

1.  **Ensure Node.js is installed**: If you don't have Node.js, download and install it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository (or copy the utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-dust-bunny-sweeper
    ```
    Or simply copy the `nightly-dust-bunny-sweeper` folder to your desired location.
3.  **No external dependencies**: This utility uses only built-in Node.js modules, so no `npm install` is strictly required within the utility's directory itself, but you might want to run `npm init -y` and `npm install jest` if you plan to run the tests.

## Usage

Run the utility from your terminal, providing the target directory to scan, the sanctuary directory to move files to, and the age threshold in days.

```bash
node src/index.js <target_directory> <sanctuary_directory> <age_threshold_days>
```

### Arguments:

*   `<target_directory>`: The path to the directory you want to scan for old files.
*   `<sanctuary_directory>`: The path to the directory where old files will be moved. This directory will be created if it doesn't exist.
*   `<age_threshold_days>`: The minimum age (in days) a file must be (based on its last modification time) to be considered a "digital dust bunny" and swept into the sanctuary.

### Example:

To sweep all files older than 90 days from your `~/Downloads` folder into a `~/DigitalDustBunnies` folder:

```bash
node src/index.js ~/Downloads ~/DigitalDustBunnies 90
```

On Windows, you might use:

```bash
node src/index.js "C:\Users\YourUser\Downloads" "C:\Users\YourUser\DigitalDustBunnies" 90
```

The utility will print a report summarizing how many files were swept and their total size.

## Development & Testing

To run the automated tests, you'll need `jest`.

1.  Navigate to the utility's directory:
    ```bash
    cd node-utils/nightly-dust-bunny-sweeper
    ```
2.  Install Jest:
    ```bash
    npm init -y
    npm install --save-dev jest
    ```
3.  Run tests:
    ```bash
    npx jest tests/index.test.js
    ```
    (Or add a `test` script to `package.json`: `"test": "jest tests/index.test.js"`)

Tests are deterministic and offline, using mocks for all file system operations to ensure reliability and speed.
