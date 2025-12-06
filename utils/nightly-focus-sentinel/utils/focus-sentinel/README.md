# Focus Sentinel: Your Digital Distraction Deflector

## Overview

In the chaotic digital landscape, staying focused can feel like a battle against an impending information apocalypse. The `Focus Sentinel` is your whimsical-yet-useful ally, designed to gently nudge you back to productivity when digital distractions loom.

This utility monitors your active window titles (or simulates this for testing) for a configurable list of 'distraction keywords.' If it spots you veering off course into the digital abyss, it'll pop up a friendly reminder to refocus or take a much-needed break.

## Features

*   **Configurable Distraction Keywords**: Easily define what constitutes a 'distraction' for you.
*   **Gentle Reminders**: Non-intrusive messages to help you regain focus.
*   **Simulated Monitoring**: Designed for easy testing and demonstration without requiring complex system integrations.

## Installation

1.  Navigate to the `utils/focus-sentinel/` directory.
2.  (Optional, but recommended) Create a Python virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows: .\venv\Scripts\activate
    ```
3.  No external dependencies are strictly required for the core logic, but `time` is used for delays.

## Usage

1.  **Configure your distractions**: The script will create a `config.json` file in the `src/` directory with default settings on its first run if one doesn't exist. You can then edit it to customize your `distraction_keywords`, `reminder_message`, and `check_interval_seconds`.
    Example `config.json`:
    ```json
    {
        "distraction_keywords": [
            "reddit",
            "twitter",
            "facebook",
            "youtube",
            "game",
            "chatgpt"
        ],
        "reminder_message": "Sentinel detected distraction! Time to refocus or take a mindful break.",
        "check_interval_seconds": 5
    }
    ```
2.  **Run the sentinel**: 
    ```bash
    python3 src/focus_sentinel.py
    ```

    The script will then start monitoring (or simulating monitoring) and provide reminders as configured. Press `Ctrl+C` to stop.

## How it Works (and How to Test)

For simplicity and cross-platform compatibility, the `focus_sentinel.py` script, in its default mode, *simulates* monitoring by checking a predefined list of window titles (when run with `simulated_titles` argument for testing). This allows for deterministic and offline testing without needing platform-specific libraries or elevated permissions.

In a real-world scenario, you would replace the `get_active_window_title_mock` function with platform-specific code (e.g., `pygetwindow` for Windows, `AppKit` for macOS, `xlib` for Linux) to truly monitor active windows. However, for this self-contained utility, the simulation is sufficient for demonstrating the core logic and enabling robust testing.

## Development & Testing

To run the tests:

```bash
python3 -m unittest tests/test_focus_sentinel.py
```
