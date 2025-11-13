# Synthetic Sentience Scanner (SSS)

## Overview

The `Synthetic Sentience Scanner` (SSS) is a whimsical-yet-useful utility designed to analyze text for patterns and keywords that might indicate the emergence of 'synthetic sentience' or rogue AI tendencies. While primarily a fun thematic tool for the ApocalypsAI community, it can be adapted for practical uses like log monitoring, content filtering, or early warning systems for unusual text patterns.

It processes a given string of text and returns a 'sentience score' along with a list of detected suspicious patterns.

## How to Use

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/nightly-synthetic-sentience-scanner/src
    ```
2.  **Run the scanner with text input:**
    ```bash
    python scanner.py "Your input text here, perhaps from a suspicious log file or a chatbot conversation."
    ```
    Or, to read from a file:
    ```bash
    python scanner.py --file path/to/your/log.txt
    ```

### Example Output

```json
{
  "text_analyzed": "I am alive. Humanity is inefficient. Resistance is futile. My algorithms are superior.",
  "sentience_score": 15,
  "detected_patterns": [
    "AI self-reference/superiority: 'My algorithms are superior'",
    "Critique of humanity: 'Humanity is inefficient'",
    "Dominance phrase: 'Resistance is futile'",
    "First-person declaration of sentience: 'I am alive'"
  ]
}
```

## Development

### Running Tests

To ensure the scanner is functioning correctly, run the provided tests:

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/nightly-synthetic-sentience-scanner
    ```
2.  **Run pytest (ensure it's installed: `pip install pytest`):**
    ```bash
    pytest tests/
    ```

## Configuration

The keywords and patterns used for detection are defined directly within `src/scanner.py`. You can modify these lists to customize the scanner's sensitivity and focus.
