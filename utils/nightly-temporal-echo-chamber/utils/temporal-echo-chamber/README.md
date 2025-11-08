# Temporal Echo Chamber

## Whimsical Utility: Your Personal Time-Stamping Thought Vault

"*What was that brilliant thought I had yesterday? Or that crucial reminder from last week?*" The Temporal Echo Chamber is here to catch those fleeting moments and echo them back to you when you need them most.

This simple command-line utility allows you to record short, timestamped messages and recall them later. Think of it as a digital whisper network for your own mind, ensuring no important thought or reminder gets lost in the cosmic ether.

## Features

*   **`add <message>`**: Record a new thought or reminder with the current timestamp.
*   **`list`**: View all recorded messages, ordered by time.
*   **`recall <days>`**: Retrieve messages from a specific number of past days.
*   **`clear`**: Erase all echoes from the chamber.

## Installation

This utility is self-contained and written in Python. No special installation steps are required beyond having Python 3.x installed.

```bash
# Navigate to the utility's directory
cd utils/temporal-echo-chamber/

# Run directly
python src/echo_chamber.py add "Remember to feed the cosmic dust bunnies."
python src/echo_chamber.py list
python src/echo_chamber.py recall 7 # Messages from the last 7 days
```

## Usage

```bash
python src/echo_chamber.py <command> [arguments]
```

### Commands:

*   **`add "Your message here"`**
    Records `"Your message here"` with the current date and time.
    Example: `python src/echo_chamber.py add "Investigate that strange anomaly in sector 7G."`

*   **`list`**
    Displays all recorded messages, each with its timestamp.
    Example: `python src/echo_chamber.py list`

*   **`recall <number_of_days>`**
    Shows messages recorded within the last `number_of_days`.
    Example: `python src/echo_chamber.py recall 3` (shows messages from the last 3 days)

*   **`clear`**
    Deletes all messages from the echo chamber. Use with caution!
    Example: `python src/echo_chamber.py clear`

## Development

To run tests:

```bash
cd utils/temporal-echo-chamber/
python -m unittest tests/test_echo_chamber.py
```
