# Nightly Cosmic Compass

Navigate the vast cosmos of your project files with the `nightly-cosmic-compass`! This whimsical-yet-useful CLI tool allows you to scan a directory, build a 'Cosmic Atlas' of its contents, and then search for 'celestial bodies' (files) and 'stellar paths' (directories) using keywords.

Think of it as a `find` command, but with a touch of intergalactic flair and type-safety.

## Features

*   **Cosmic Atlas Generation**: Recursively scans a specified directory to map all files and subdirectories.
*   **Keyword Search**: Quickly locate files and directories by name or path using one or more keywords.
*   **Whimsical Output**: Presents search results with cosmic-themed terminology and emoji.
*   **Type-Safe**: Built with TypeScript for robust and predictable behavior.

## Installation

To use the Cosmic Compass, you'll need Node.js (v14 or higher) and npm/yarn installed.

1.  **Clone the repository (or copy the utility folder):**

    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-cosmic-compass
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    # or yarn install
    ```

## Usage

Run the Cosmic Compass from the utility's root directory. You must provide a target path (directory) to explore.

### Basic Scan (Build the Cosmic Atlas)

To simply scan a directory and build its atlas without searching:

```bash
npm start <path-to-your-project>
# Example: npm start .
```

This will output a message indicating the atlas has been built and how many 'celestial bodies' were mapped.

### Searching for Celestial Bodies

Use the `--search` or `-s` option followed by one or more keywords to find specific files or directories.

```bash
npm start <path-to-your-project> -- --search <keyword1> [keyword2...]
# Example: npm start . -- --search component ts
# Example: npm start ../../ -- -s readme config
```

**Note**: The `--` before `--search` is important when running via `npm start` to pass arguments directly to the underlying script.

#### Example Output:

```
Initiating Cosmic Scan of: /home/user/my-project
Searching for cosmic anomalies matching: component, ts

2 celestial bodies detected:
  ⭐ src/components/Button.ts
    - Found 'component' in path/name
    - Found 'ts' in path/name
  🌌 src/components
    - Found 'component' in path/name
```

### Running Tests

To ensure the Cosmic Compass is functioning correctly, run the automated tests:

```bash
npm test
```

## Development

If you wish to modify or extend the Cosmic Compass:

1.  **Build the TypeScript code:**

    ```bash
    npm run build
    ```

    This compiles the TypeScript files in `src/` into JavaScript in the `dist/` directory.

2.  **Run the compiled code:**

    ```bash
    node dist/cli.js <path-to-your-project> -- --search <keywords...>
    ```

## Contributing

Feel free to suggest improvements or new cosmic features! May your navigation be ever true.
