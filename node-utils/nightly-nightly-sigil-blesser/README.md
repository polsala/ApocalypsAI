# nightly-sigil-blesser

A Node.js CLI tool that bestows unique, whimsical "digital sigils" upon your files. Each sigil is a mystical combination of the file's essence (a hash) and a randomly chosen adjective-noun pair, logged for posterity in the `sigils.json` ledger. Perfect for marking important data, or simply adding a touch of arcane charm to your digital hoard.

## Installation

1.  Navigate to the `node-utils/nightly-sigil-blesser` directory.
2.  Install dependencies (if any, though this utility aims to be dependency-free):
    ```bash
    # No external dependencies needed for this utility!
    ```

## Usage

Run the utility from your terminal, providing the path to the file you wish to bless:

```bash
node src/index.js <file_path>
```

### Example

```bash
node src/index.js ./my_secret_plans.txt
```

Output:
```
File blessed!
Sigil: 8b1a99d4-Whispering-Orb
Logged to: sigils.json
```

## How it Works

1.  **File Essence**: The tool reads the content of your specified file and generates an MD5 hash, representing its unique digital fingerprint.
2.  **Whimsical Adornment**: It then selects a random adjective (e.g., "Whispering", "Rusty", "Silent") and a random noun (e.g., "Orb", "Cog", "Echo") from its internal lexicon.
3.  **Sigil Creation**: These two elements are combined with the hash to form a unique "digital sigil" (e.g., `8b1a99d4-Whispering-Orb`).
4.  **Ledger Entry**: The sigil, along with the file path and timestamp, is recorded in a `sigils.json` file in the utility's root directory, creating a historical record of all blessed items.
5.  **Output**: The newly generated sigil is displayed to the user.

## Sigil Log (`sigils.json`) Format

The `sigils.json` file will contain an array of objects, each representing a blessed file:

```json
[
  {
    "timestamp": "2023-10-27T10:30:00.000Z",
    "filePath": "/path/to/your/file.txt",
    "sigil": "8b1a99d4-Whispering-Orb"
  },
  {
    "timestamp": "2023-10-27T11:15:00.000Z",
    "filePath": "/another/path/to/data.json",
    "sigil": "a1b2c3d4-Silent-Echo"
  }
]
```
