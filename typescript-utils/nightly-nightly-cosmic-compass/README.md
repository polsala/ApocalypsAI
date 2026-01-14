# Nightly Cosmic Compass

A whimsical command-line utility that offers cosmically-aligned path recommendations based on a given cardinal direction. When the path ahead is unclear, let the cosmos whisper its guidance.

## Usage

```bash
npx ts-node src/index.ts <direction>
# or, after building:
# node dist/index.js <direction>
```

Replace `<direction>` with one of `N`, `S`, `E`, or `W`. Case-insensitive.

### Examples

```bash
npx ts-node src/index.ts N
# Output: "To the N: Follow the faint echo of the void, where forgotten stars hum."

npx ts-node src/index.ts west
# Output: "To the W: Veer slightly towards the shimmering nebula, seeking nascent truths."

npx ts-node src/index.ts X
# Output: "Error: Invalid direction. Please use N, S, E, or W."
```

## Development

1.  **Install dependencies**:
    ```bash
    npm install
    ```
2.  **Run directly**:
    ```bash
    npx ts-node src/index.ts N
    ```
3.  **Build**:
    ```bash
    npm run build
    ```
4.  **Run built version**:
    ```bash
    node dist/index.js N
    ```
5.  **Run tests**:
    ```bash
    npm test
    ```
