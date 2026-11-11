# Nightly Whimsical Mood Analyzer

## Summary

The `nightly-whimsical-mood-analyzer` is a command-line utility designed to process text input (from files or stdin) and categorize its overall 'whimsical mood'. It assigns a sentiment score based on predefined keywords, classifying the text into moods like `GloomDoom`, `HopeSpark`, `ChaosChuckle`, and `VoidZen`. This tool helps the ApocalypsAI community quickly gauge the emotional or thematic tone of generated logs, messages, or other textual outputs.

## Whimsical Moods

*   **GloomDoom**: Reflects despair, destruction, and the inevitable end.
*   **HopeSpark**: Indicates optimism, rebuilding, and the potential for a better future.
*   **ChaosChuckle**: Captures playful unpredictability, mischief, and delightful disorder.
*   **VoidZen**: Represents calm, emptiness, profound stillness, and detached observation.

## Installation

1.  **Clone the repository (if not already done):**
    ```bash
    git clone https://github.com/polsala/ApocalypsAI.git
    cd ApocalypsAI/typescript-utils/nightly-whimsical-mood-analyzer
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Build the TypeScript project:**
    ```bash
    npm run build
    ```

## Usage

The utility can read text from a file or directly from standard input.

### From a file:

```bash
node dist/index.js --file <path/to/your/textfile.txt>
```

### From standard input (piping):

```bash
cat <path/to/your/textfile.txt> | node dist/index.js
# Or, for interactive input:
echo "The void whispers of impending doom, yet a spark of hope flickers amidst the chaos."
```

### Example Output (JSON):

```json
{
  "totalLines": 1,
  "totalWords": 16,
  "moodCounts": {
    "GloomDoom": 1,
    "HopeSpark": 1,
    "ChaosChuckle": 1,
    "VoidZen": 1
  },
  "dominantMood": "Mixed",
  "moodDistribution": {
    "GloomDoom": 0.25,
    "HopeSpark": 0.25,
    "ChaosChuckle": 0.25,
    "VoidZen": 0.25
  }
}
```

## Development

To run tests:

```bash
npm test
```
