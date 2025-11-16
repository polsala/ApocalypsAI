# Nightly Survival Skill Scribe

## 📜 Overview

The ApocalypsAI Nightly Survival Skill Scribe is a whimsical-yet-useful command-line utility designed to be your quick-reference guide for essential survival knowledge. In times of chaos or just for general preparedness, having concise, actionable steps for critical skills can make all the difference. From purifying water to starting a fire, the Scribe has you covered with its curated database of vital information.

## ✨ Features

*   **List Skills**: See all available survival skills at a glance.
*   **Get Details**: Retrieve detailed, step-by-step instructions for any specific skill.
*   **Search**: Find skills by keywords, titles, or descriptions.

## 🚀 How to Use

This utility is a Python 3.11 script. You can run it directly from its directory.

### Prerequisites

*   Python 3.11 or higher

### Commands

Navigate to the `src` directory within `nightly-survival-skill-scribe` and run `scribe.py` with the desired action.

1.  **List all available skills:**
    ```bash
    python3 src/scribe.py list
    ```

2.  **Get detailed instructions for a specific skill:**
    ```bash
    python3 src/scribe.py get water_purification
    ```
    (Replace `water_purification` with the key of the skill you want to learn about, e.g., `basic_first_aid`, `fire_starting`).

3.  **Search for skills by a keyword or phrase:**
    ```bash
    python3 src/scribe.py search fire
    ```
    ```bash
    python3 src/scribe.py search aid
    ```

## 🧪 Testing

To run the tests for this utility, navigate to the `nightly-survival-skill-scribe` directory and execute:

```bash
python3 -m unittest tests/test_scribe.py
```

All tests are self-contained and deterministic, using in-memory data and mocking `sys.stdout` and `sys.exit` to ensure reliable, offline execution.
