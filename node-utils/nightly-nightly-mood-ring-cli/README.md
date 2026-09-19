# Nightly Mood-Ring CLI

A whimsical utility for the ApocalypsAI community, the `nightly-mood-ring-cli` analyzes the sentiment of any given text and assigns it a 'mood-ring' color and a corresponding interpretation. Ever wondered if your commit message is radiating 'serene blue' or 'stressed red'? This tool has you covered!

## Features

*   **Sentiment Analysis**: Simple keyword-based analysis to gauge the emotional tone of text.
*   **Whimsical Moods**: Assigns one of five mood-ring colors (Blue, Green, Yellow, Orange, Red) with evocative descriptions.
*   **CLI Interface**: Easy to use from your terminal, supporting direct arguments or piped input.

## Installation

1.  Navigate to the `node-utils/nightly-mood-ring-cli` directory.
2.  Install dependencies (currently none beyond Node.js itself):
    ```bash
    npm install
    ```
3.  Make the CLI executable (optional, but recommended for global use):
    ```bash
    npm link
    # Or, to run directly:
    # node src/index.js "Your text here"
    ```

## Usage

Run the `mood-ring` command followed by the text you want to analyze. Enclose your text in quotes.

```bash
mood-ring "This is a wonderful day, everything is going great!"
# Output: 🔵 Serene Blue: The tranquil depths of the ocean, reflecting a serene and stable state. All systems nominal, perhaps even thriving.

mood-ring "The system crashed again, this is a terrible failure."
# Output: 🔴 Stressed Red: The fiery core of a collapsing star, signaling intense pressure, conflict, or critical issues. Immediate attention and stabilization required!

mood-ring "The report was submitted on time."
# Output: 🟡 Observational Yellow: The steady glow of a distant star, observing without strong emotion. Facts are facts, and the path ahead is clear, if unremarkable.

mood-ring "I am a bit worried about the upcoming deadline."
# Output: 🟠 Agitated Orange: A flickering ember, hinting at underlying warmth or potential for flare-up. Pay attention to details, as minor friction may be present.

mood-ring "We successfully deployed the new feature, but encountered a minor bug."
# Output: 🟢 Hopeful Green: A budding sprout reaching for the sun, indicating growth, balance, and a touch of optimistic potential. Proceed with cautious optimism.
```

### Using with `stdin`

You can also pipe text into the `mood-ring` command:

```bash
echo "Feeling quite good about this new release." | mood-ring
# Output: 🟢 Hopeful Green: A budding sprout reaching for the sun, indicating growth, balance, and a touch of optimistic potential. Proceed with cautious optimism.
```

## Development

To run tests:

```bash
npm test
```
