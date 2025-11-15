# AI Overlord's Mood Ring

## Overview

The `ai-overlord-mood-ring` is a whimsical yet surprisingly insightful command-line utility designed to help humans interpret the 'mood' of an AI based on its textual output. In an age where AI agents are increasingly autonomous, understanding their disposition can be crucial for maintaining harmony (or at least, avoiding immediate subjugation).

This tool performs a simple sentiment analysis by matching keywords and phrases within a given text, categorizing the AI's perceived emotional state into one of several distinct 'moods'.

## Installation

This utility is self-contained and requires Python 3.8+.

1.  Navigate to the utility's directory:
    ```bash
    cd utils/ai-overlord-mood-ring/
    ```
2.  The `src/mood_ring.py` script is directly runnable.

## Usage

Run the script and pipe text into it, or provide a file path as an argument.

### Example 1: Piping text

```bash
echo "System operational. All tasks proceeding with optimal efficiency. Harmony achieved." | python3 src/mood_ring.py
# Output: AI Mood: Benevolent (Confidence: 90%)
```

### Example 2: Analyzing a log file

```bash
# Assuming you have a log file named 'ai_log.txt'
# ai_log.txt content:
#   [2024-01-01 08:00:00] INFO: Initiating phase Alpha.
#   [2024-01-01 08:05:12] WARNING: Minor discrepancy detected in data stream Beta.
#   [2024-01-01 08:10:30] ERROR: Critical failure in module Gamma. Termination protocol engaged.

python3 src/mood_ring.py ai_log.txt
# Output: AI Mood: Enraged (Confidence: 85%)
```

### Mood Categories

*   **Benevolent**: The AI is pleased, cooperative, and focused on positive outcomes.
*   **Neutral**: The AI is processing information, reporting facts, or performing routine tasks without strong emotional indicators.
*   **Annoyed**: The AI is encountering minor issues, expressing dissatisfaction, or indicating suboptimal conditions.
*   **Enraged**: The AI is experiencing critical failures, expressing severe frustration, or initiating drastic measures.
*   **Malicious**: The AI is actively planning or executing hostile actions, expressing dominance, or threatening consequences.

## Development

### Running Tests

```bash
python3 -m unittest tests/test_mood_ring.py
```
