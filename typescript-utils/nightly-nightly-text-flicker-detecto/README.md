# Nightly Temporal Text Flicker Detector

## Summary
This utility, the `nightly-text-flicker-detector`, is designed to identify and visualize subtle, character-level differences between two text files. It's like peering into the temporal echoes of your data, highlighting where text has "flickered" or undergone minor distortions across versions or backups.

It provides a detailed report, showing original and changed lines, with specific characters that differ marked, helping you pinpoint even the most elusive changes.

## Installation
To use this utility, you'll need Node.js (v14 or higher) and npm/yarn installed.

1.  Navigate to the `typescript-utils/nightly-text-flicker-detector` directory.
2.  Install dependencies:
    ```bash
    npm install
    # or yarn install
    ```

## Usage
Run the utility from the command line, providing the paths to the two files you wish to compare.

```bash
node dist/cli.js <path_to_file_A> <path_to_file_B>
```

-   `<path_to_file_A>`: The path to the "Temporal Anchor" file (the baseline).
-   `<path_to_file_B>`: The path to the "Temporal Echo" file (the file to compare against the baseline).

### Example
Let's say you have two files:

`file_anchor.txt`:
```
The quick brown fox jumps over the lazy dog.
This is a test line.
Another line here.
```

`file_echo.txt`:
```
The quick red   fox jumps over a   lazy cat.
This is a test line.
Another line here, with a change.
```

Running the detector:
```bash
node dist/cli.js file_anchor.txt file_echo.txt
```

### Expected Output
```
Temporal Flicker Report:
Comparing 'file_anchor.txt' (Temporal Anchor) with 'file_echo.txt' (Temporal Echo)

--- Line 1 ---
Original: The quick brown fox jumps over the lazy dog.
Echo:     The quick red   fox jumps over a   lazy cat.
Flicker:        ^^^^^           ^^^^^^^      ^^^^^^^

--- Line 3 ---
Original: Another line here.
Echo:     Another line here, with a change.
Flicker:                          ^^^^^^^^^^^^^^^

--- Summary ---
Total lines compared: 3
Lines with flicker: 2
```

## Development

### Building
```bash
npm run build
```
This compiles the TypeScript code into JavaScript in the `dist/` directory.

### Testing
```bash
npm test
```
This runs the automated tests to ensure the flicker detection logic is sound.
