# Nightly Digital Dust Purifier

## 🌌 Overview

In the post-apocalyptic digital wasteland, data can accumulate "digital dust" – extraneous whitespace, phantom empty lines, and cryptic non-printable characters that obscure its true essence. The `Nightly Digital Dust Purifier` is a whimsical yet essential Node.js CLI utility designed to meticulously cleanse your text files, restoring their pristine form and making them readable for even the most discerning data archaeologists.

It's like a spa day for your text, ensuring every character is where it should be, and no digital detritus remains.

## ✨ Features

*   **Whitespace Annihilation**: Trims leading and trailing whitespace from every line.
*   **Empty Line Consolidation**: Reduces multiple consecutive empty lines to a single, dignified empty line.
*   **Non-Printable Character Expulsion**: Banishes invisible, non-printable ASCII characters that can cause rendering issues or data corruption.
*   **Cross-Platform Compatibility**: Built with Node.js, it runs wherever Node.js runs.

## 🚀 Installation

1.  **Ensure Node.js is installed**: If not, download it from [nodejs.org](https://nodejs.org/).
2.  **Clone the repository (or download this utility)**:
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-digital-dust-purifier
    ```
3.  **Install dependencies**: This utility uses `jest` for testing. While the core logic has no external runtime dependencies, `jest` needs to be installed for tests.
    ```bash
    npm install
    ```

## 🛠️ Usage

Run the utility from its directory:

```bash
node src/index.js <input_file_path> [output_file_path]
```

*   `<input_file_path>`: The path to the text file you wish to purify.
*   `[output_file_path]`: (Optional) The path where the purified content will be saved. If omitted, the purified content will be printed to `stdout`.

### Examples:

1.  **Purify a file and print to console:**
    ```bash
    node src/index.js my_dusty_log.txt
    ```
2.  **Purify a file and save to a new file:**
    ```bash
    node src/index.js old_manifest.txt new_manifest_purified.txt
    ```
3.  **Purify a file and overwrite the original (use with caution!):**
    ```bash
    node src/index.js important_notes.txt important_notes.txt
    ```

## 🧪 Tests

To run the automated tests:

```bash
npm test
```

The tests ensure the purifier functions correctly under various conditions, including handling empty files, excessive whitespace, and non-printable characters.
