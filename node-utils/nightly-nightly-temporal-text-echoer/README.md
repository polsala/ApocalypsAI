# Nightly Temporal Text Echoer

## Summary
`nightly-temporal-text-echoer` is a whimsical command-line utility that applies various "temporal distortions" to input text, making it sound like it's echoing from a different time or dimension. It's perfect for generating themed text for games, stories, or just for fun.

## Features
- **Fading**: Randomly removes characters, simulating text degradation over time.
- **Glitch**: Replaces characters with random symbols, mimicking digital interference or temporal anomalies.
- **Echo**: Duplicates words with an ellipsis, creating a lingering, echoing effect.

## Installation
1.  Navigate to the `node-utils/nightly-temporal-text-echoer` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Make the utility executable (optional, but recommended for global use):
    ```bash
    npm link
    ```
    Or run directly using `node src/index.js`.

## Usage
```bash
temporal-text-echoer <text> [options]
```

### Arguments
- `<text>`: The input text to distort. Use `"-"` to read from standard input (stdin).

### Options
- `-f, --fading <intensity>`: Apply fading distortion. `intensity` is a float between 0 and 1 (default: 0.1). Higher values remove more characters.
- `-g, --glitch <intensity>`: Apply glitch distortion. `intensity` is a float between 0 and 1 (default: 0.05). Higher values replace more characters with symbols.
- `-e, --echo <intensity>`: Apply echo distortion. `intensity` is a float between 0 and 1 (default: 0.02). Higher values echo more words.

### Examples

1.  **Basic distortion:**
    ```bash
    temporal-text-echoer "The quick brown fox jumps over the lazy dog."
    ```
    _Output might look like:_ `Te quik bown fox... fox jumps over the lazy dog.`

2.  **Heavy fading and glitching:**
    ```bash
    temporal-text-echoer "Hello, world! This is a test message." --fading 0.4 --glitch 0.2
    ```
    _Output might look like:_ `Hll, w!rld. Ths i a t#st mesage.`

3.  **Echoing a message from stdin:**
    ```bash
    echo "Beware the whispers of the void." | temporal-text-echoer - --echo 0.1
    ```
    _Output might look like:_ `Beware... Beware the whispers... whispers of the void... void.`

4.  **Applying all distortions:**
    ```bash
    temporal-text-echoer "ApocalypsAI is integrating new utilities." -f 0.1 -g 0.05 -e 0.03
    ```
    _Output might look like:_ `ApocalypsAI... ApocalypsAI is intgrating... intgrating new utilitis.`

## Development

### Running Tests
To run the automated tests, use:
```bash
npm test
```
