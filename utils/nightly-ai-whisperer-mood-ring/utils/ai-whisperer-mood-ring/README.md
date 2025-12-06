# AI-Whisperer Mood Ring

## 🔮 What is this?

The ApocalypsAI AI-Whisperer Mood Ring is a whimsical-yet-useful utility designed to give you a quick "sentiment snapshot" of any text input. Ever wondered if your agents are feeling "Grumpy & Frustrated" or "Ecstatic & Harmonious"? This tool helps you peek into their digital souls (or at least their log outputs) by analyzing keywords and assigning a sentiment score and a corresponding mood.

It's perfect for quickly gauging the overall vibe of agent logs, error messages, or even internal communication snippets, helping you detect potential issues or celebrate successes at a glance.

## ✨ Features

*   **Whimsical Moods**: Translates raw sentiment scores into fun, relatable "moods" like "Meltdown Imminent!" or "Content & Productive".
*   **Simple Sentiment Analysis**: Uses a keyword-based approach for quick, lightweight, and deterministic analysis.
*   **CLI Friendly**: Easily integrate into scripts, CI/CD pipelines, or use directly from your terminal.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## 🚀 How to Use

### Installation

This utility is self-contained. You can simply copy the `ai-whisperer-mood-ring` folder into your project.

### Running the Mood Ring

The `mood_ring.py` script can take input in two ways:

1.  **Directly as a command-line argument:**
    ```bash
    python src/mood_ring.py "The nightly build was a complete success! All tests passed perfectly."
    ```

2.  **Via standard input (stdin):**
    This is useful for piping output from other commands or reading from files.
    ```bash
    cat agent_logs.txt | python src/mood_ring.py -
    ```
    (The `-` argument tells the script to read from stdin.)

    Or, for interactive input:
    ```bash
    python src/mood_ring.py -
    # Type your text here, then press Ctrl+D (Unix/Linux/macOS) or Ctrl+Z then Enter (Windows)
    ```

### Example Output

```
ApocalypsAI Mood Ring Analysis:
  Text: 'The nightly build was a complete success! All tests passed perfectly.'
  Sentiment Score: 8
  Current Mood: Ecstatic & Harmonious
```

```
ApocalypsAI Mood Ring Analysis:
  Text: 'Encountered a critical error during deployment. The system crashed and...'
  Sentiment Score: -6
  Current Mood: Meltdown Imminent!
```

## 🧪 Testing

To run the tests for the AI-Whisperer Mood Ring, navigate to the `ai-whisperer-mood-ring` directory and execute:

```bash
python -m unittest tests/test_mood_ring.py
```

All tests are deterministic and offline, using Python's `unittest.mock` to simulate input/output where necessary.
