# 🌟 Nightly Optimism Orb Log Analyzer 🌟

## Overview

The `Nightly Optimism Orb Log Analyzer` is a whimsical-yet-useful utility designed to bring a daily dose of digital sunshine to your systems. In the vast, often chaotic, landscape of logs, this orb sifts through the noise to highlight moments of success, completion, and progress. It scans specified directories for log files, identifies positive keywords, and generates a heartwarming report summarizing the good news.

Think of it as your personal digital cheerleader, ensuring that even amidst the apocalypse, you don't miss the small victories!

## Features

*   **Positive Keyword Detection**: Scans `.log` and `.txt` files for a predefined set of positive keywords (e.g., `success`, `completed`, `healthy`, `progress`).
*   **Customizable Keywords**: Extend the orb's vocabulary with your own project-specific positive terms.
*   **Recursive Directory Scan**: Delves into subdirectories to ensure no positive log entry is overlooked.
*   **Markdown Report Generation**: Produces a clean, readable summary report, perfect for sharing or quick review.
*   **Error Handling**: Gracefully handles unreadable files or non-existent directories.

## Usage

### Prerequisites

*   Python 3.8+ (tested with 3.11)

### Running the Analyzer

1.  Navigate to the `utils/nightly-optimism-orb-log-analyzer` directory.
2.  Run the `orb_analyzer.py` script with the path to your log directory:

    ```bash
    python src/orb_analyzer.py /path/to/your/log/directory
    ```

    **Example:**
    ```bash
    python src/orb_analyzer.py /var/log/my_app
    ```

### Adding Custom Keywords

You can provide additional positive keywords using the `--keywords` argument. These will be added to the orb's default set.

```bash
python src/orb_analyzer.py /path/to/your/log/directory --keywords "deployed_successfully" "feature_enabled" "user_happy"
```

### Example Output

```markdown
# 🌟 Nightly Optimism Orb Report 🌟

Greetings, fellow cosmic travelers! The Optimism Orb has spun its magic,
sifting through the digital ether to bring you a beacon of positivity.

## ✨ Summary of Digital Sunshine ✨
**Total Positive Mentions Found:** `8` across `2` files.

The universe whispers its successes through these keywords:

- `success`: `5` times
- `completed`: `2` times
- `progress`: `1` times

## 📜 Files Scanned 📜
- `/var/log/my_app/app.log`
- `/var/log/my_app/worker.log`

---
May your systems be stable and your spirits high!
```

## Development & Testing

### Running Tests

To ensure the Optimism Orb is always shining brightly, run its self-contained tests:

1.  Navigate to the `utils/nightly-optimism-orb-log-analyzer` directory.
2.  Execute the tests using `unittest`:

    ```bash
    python -m unittest tests/test_orb_analyzer.py
    ```

The tests are designed to be deterministic and offline, using mocks to simulate file system interactions and file contents.
