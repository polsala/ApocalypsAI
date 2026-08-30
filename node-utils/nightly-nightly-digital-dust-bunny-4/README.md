# nightly-digital-dust-bunny

## 🗑️ Digital Dust Bunny Sweeper

In the quiet corners of your digital wasteland, forgotten files accumulate like dust bunnies, silently consuming precious storage and mental bandwidth. The `nightly-digital-dust-bunny` utility is your trusty broom, designed to sweep through specified directories, identify these long-neglected "digital dust bunnies," and help you reclaim your digital space.

It reports files that haven't been modified in a configurable period, allowing you to decide whether to archive, delete, or simply acknowledge their existence.

## ✨ Features

-   **Recursive Scanning**: Traverses directories and their subdirectories.
-   **Age-Based Filtering**: Identifies files older than a specified duration (days, months, or years).
-   **Clear Reporting**: Lists detected dust bunnies with their last modification date.
-   **Cross-Platform**: Built with Node.js, runs wherever Node.js does.

## 🚀 Installation

1.  **Ensure Node.js is installed**: If not, download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository (or just this utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-bunny
    ```
3.  **Install dependencies**:
    ```bash
    npm install
    ```

## 🛠️ Usage

Run the utility from its directory:

```bash
node src/index.js --path <directory_to_scan> [--age <number>] [--unit <days|months|years>]
```

### Arguments:

-   `--path <directory_to_scan>`: **Required**. The absolute or relative path to the directory you want to scan for digital dust bunnies.
-   `--age <number>`: **Optional**. The number representing the age threshold. Files older than this will be reported. Defaults to `90`.
-   `--unit <days|months|years>`: **Optional**. The unit for the `--age` argument. Defaults to `days`.

### Examples:

Scan your `old_projects` folder for files older than 180 days:
```bash
node src/index.js --path /home/user/old_projects --age 180 --unit days
```

Find files in your `downloads` directory that haven't been touched in over 2 years:
```bash
node src/index.js --path ./downloads --age 2 --unit years
```

Scan the current directory for files older than 3 months (using default age 90 days):
```bash
node src/index.js --path . --age 3 --unit months
```

## 🧪 Tests

To run the automated tests:

```bash
npm test
```
