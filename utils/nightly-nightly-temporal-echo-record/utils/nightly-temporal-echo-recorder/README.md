# Nightly Temporal Echo Recorder

## 🌌 Capture Whispers from the Void 🌌

The Nightly Temporal Echo Recorder is a whimsical yet practical utility designed to help you quickly jot down fleeting thoughts, commands, or critical observations before they vanish into the temporal ether. Think of it as a cosmic sticky note pad, timestamped and searchable, ready to recall the whispers of yesterday.

### ✨ Features

*   **Record Echoes**: Save any text snippet with an automatic timestamp.
*   **List Echoes**: View all your recorded whispers, ordered by their temporal appearance (most recent first).
*   **Search Echoes**: Find specific echoes using keywords, retrieving them from the depths of the void.
*   **Purge Old Echoes**: Automatically clean up echoes older than a specified duration, preventing the void from becoming too cluttered.

### 🚀 Usage

The utility is a Python script that can be run from the command line.

#### Prerequisites

*   Python 3.6+

#### Commands

```bash
# Add a new echo
python src/echo_recorder.py add "My fleeting thought about the cosmic alignment."

# List all echoes
python src/echo_recorder.py list

# Search echoes containing a keyword (case-insensitive)
python src/echo_recorder.py search "cosmic"

# Purge echoes older than 7 days
python src/echo_recorder.py purge 7
```

### 🛠️ Development

The echoes are stored in a simple JSON file (`echoes.json`) within the utility's directory.

#### Running Tests

```bash
python -m unittest tests/test_echo_recorder.py
```
