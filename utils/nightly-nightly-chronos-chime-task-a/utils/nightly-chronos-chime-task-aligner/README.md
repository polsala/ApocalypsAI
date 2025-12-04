# Chronos-Chime Task Aligner

A whimsical command-line utility designed to help you align your focus and recharge your energies using a Pomodoro-like technique. Let the Chronos-Chime guide you through focused work sessions and rejuvenating breaks, ensuring optimal productivity in the face of any apocalypse (or just a busy Tuesday).

## Features

*   **Configurable Work Sessions**: Set the duration for your focused work periods.
*   **Configurable Breaks**: Define the length of your short breaks.
*   **Cycle Management**: Specify how many work-break cycles you want to complete.
*   **Whimsical Chimes**: Console messages signal transitions between work and break, keeping you aligned.
*   **Graceful Interruption**: Easily stop the timer at any point with `Ctrl+C`.

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

1.  Navigate to the `utils/nightly-chronos-chime-task-aligner/` directory.
2.  The `src/chronos_chime.py` file is the main runnable script.

## Usage

Run the `chronos_chime.py` script directly from your terminal:

```bash
python src/chronos_chime.py
```

### Options:

*   `-w`, `--work <minutes>`: Duration of each work session in minutes. Default is 25 minutes.
*   `-b`, `--break <minutes>`: Duration of each short break in minutes. Default is 5 minutes.
*   `-c`, `--cycles <number>`: Number of work-break cycles to complete. Default is 4 cycles.

### Examples:

1.  **Start with default settings (25 min work, 5 min break, 4 cycles):**
    ```bash
    python src/chronos_chime.py
    ```

2.  **Custom work and break times (e.g., 45 min work, 10 min break):**
    ```bash
    python src/chronos_chime.py --work 45 --break 10
    ```

3.  **Run only 2 cycles:**
    ```bash
    python src/chronos_chime.py --cycles 2
    ```

4.  **A quick 1-minute focus session with a 30-second break, 3 times (for testing or very short tasks):**
    ```bash
    python src/chronos_chime.py -w 1 -b 0.5 -c 3
    ```

## Development & Testing

To run the automated tests:

1.  Navigate to the `utils/nightly-chronos-chime-task-aligner/` directory.
2.  Execute the tests using `unittest`:
    ```bash
    python -m unittest tests/test_chronos_chime.py
    ```

The tests are designed to be deterministic and run offline, using mocks for `time.sleep` and `sys.stdout` to simulate timer progression and capture output without actual delays.
