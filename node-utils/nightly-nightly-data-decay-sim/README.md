# nightly-data-decay-sim

A whimsical-yet-useful Node.js CLI utility that simulates data corruption on text files over "time" (iterations). This tool can be used to generate corrupted test data for robust parsing, create artistic "decayed" text, or simply for fun.

## 🌌 Purpose

In the post-apocalyptic digital age, data integrity is a fleeting dream. The `nightly-data-decay-sim` helps you understand the fragility of information by simulating the gradual corruption of text files. Watch your pristine data succumb to the cosmic background radiation, temporal anomalies, or just plain digital rot.

## ✨ Features

*   **Configurable Decay**: Adjust the number of decay iterations and the probability of corruption per character.
*   **Multiple Decay Types**: Characters can be replaced, deleted, or have random symbols inserted.
*   **File I/O**: Read from an input file and optionally write the decayed output to a new file or print to stdout.
*   **Cross-Platform**: Runs anywhere Node.js is supported.

## 🚀 Installation

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/node-utils/nightly-data-decay-sim
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    ```

## 🛠️ Usage

Run the utility from the command line:

```bash
node src/index.js <filePath> [iterations] [decayRate] [outputPath]
```

### Arguments:

*   `<filePath>` (required): The path to the text file you want to decay.
*   `[iterations]` (optional): The number of decay passes to apply. Each pass further corrupts the data. Defaults to `1`.
*   `[decayRate]` (optional): A float between `0.0` and `1.0` representing the probability that a character will decay during a pass. Defaults to `0.05` (5%).
*   `[outputPath]` (optional): The path to save the decayed content. If omitted, the decayed content will be printed to `stdout`.

### Examples:

1.  **Decay a file once, print to console:**
    ```bash
    echo "The quick brown fox jumps over the lazy dog." > original.txt
    node src/index.js original.txt
    ```
    (Output will be a slightly corrupted version of the text)

2.  **Decay a file 5 times with a higher decay rate, save to a new file:**
    ```bash
    node src/index.js original.txt 5 0.15 decayed_message.txt
    cat decayed_message.txt
    ```
    (The `decayed_message.txt` will contain a more heavily corrupted version)

3.  **Generate a very corrupted message quickly:**
    ```bash
    echo "Secret plans for the last remaining can of beans." > secret_plans.txt
    node src/index.js secret_plans.txt 10 0.25
    ```

## 🧪 Tests

To run the automated tests:

```bash
npm test
```

The tests are deterministic and offline, using mocks for file system operations and `Math.random` to ensure consistent results.

## 📜 License

This utility is released under the MIT License. See the main repository's `LICENSE` file for more details.
