# AI Overlord Mood Ring

## Overview

The AI Overlord Mood Ring is a whimsical utility designed to give you a quick, human-readable insight into the "mood" of your system, as if it were an all-powerful AI overlord. By analyzing key system metrics like CPU, memory, and disk usage, it translates raw data into a simple emotional state, helping you gauge system health at a glance. Is the Overlord "Content" or "Agitated"? Find out!

## Features

*   **System Metric Analysis**: Gathers CPU, memory, and disk usage (simulated for demonstration).
*   **Mood Translation**: Converts numerical metrics into one of several predefined "moods."
*   **Whimsical Output**: Provides a fun, yet informative, summary of your system's state.

## Installation

This utility is self-contained and requires Python 3.11+.

1.  Navigate to the `utils/ai-overlord-mood-ring/` directory.
2.  (Optional) Create a virtual environment: `python3 -m venv .venv`
3.  (Optional) Activate the virtual environment: `source .venv/bin/activate`

## Usage

To get the current "mood" of your AI Overlord:

```bash
python3 src/mood_ring.py
```

Example Output:

```
The AI Overlord is feeling: Content. All systems nominal.
```

or

```
The AI Overlord is feeling: Agitated. High CPU usage detected.
```

## Configuration

Currently, there are no configurable parameters. The thresholds for mood changes are hardcoded within `src/mood_ring.py`.

## Development & Testing

To run the tests:

```bash
python3 -m unittest tests/test_mood_ring.py
```
