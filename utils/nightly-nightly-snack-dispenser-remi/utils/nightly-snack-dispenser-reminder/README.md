# Nightly Snack Dispenser Reminder

## 🍎 Fuel Your Apocalypse! 🍪

In the relentless grind of post-apocalyptic survival (or just a particularly demanding coding session), it's easy to forget the most crucial resource: **YOU!** The Nightly Snack Dispenser Reminder is a whimsical-yet-vital utility designed to gently nudge you towards taking a much-needed break and refueling your internal systems. Because even the most hardened survivor needs a cookie. Or a protein bar. Or a handful of irradiated berries (consume at your own risk).

## ✨ Features

*   **Timely Nudges**: Configured to remind you at optimal "refueling" intervals during your day.
*   **Whimsical Messaging**: Delivers fun, apocalypse-themed prompts to encourage your snack breaks.
*   **Lightweight & Self-Contained**: A simple Python script with no external dependencies, easy to integrate into your daily routine.

## 🚀 How to Use

1.  **Navigate**: Change into the utility's directory:
    ```bash
    cd utils/nightly-snack-dispenser-reminder/src
    ```
2.  **Run**: Execute the script directly:
    ```bash
    python reminder.py
    ```
    If it's a designated snack time, you'll see a message like:
    ```
    🚨 APOCALYPSE ALERT! 🚨 Your internal energy reserves are critically low! Time for a tactical snack deployment! Go forth and refuel!
    ```
    Otherwise, it will run silently.

3.  **Automate (Optional but Recommended for Optimal Survival)**:
    For continuous well-being, consider adding this script to your system's scheduler (e.g., `cron` on Linux/macOS, Task Scheduler on Windows) to run every 30 minutes or hour.

    **Example Cron Entry (runs every 30 minutes):**
    ```cron
    */30 * * * * /usr/bin/python3 /path/to/your/repo/utils/nightly-snack-dispenser-reminder/src/reminder.py >> /tmp/snack_log.txt 2>&1
    ```
    *(Remember to replace `/path/to/your/repo/` with the actual path to your ApocalypsAI repository.)*

## ⚙️ Configuration

The default snack times are set for typical mid-morning, post-lunch, and late-afternoon boosts. You can easily customize these by editing the `SNACK_TIMES` list in `src/reminder.py`.

```python
# src/reminder.py
SNACK_TIMES = [
    (10, 30),  # Mid-morning fuel-up
    (13, 30),  # Post-lunch energy boost
    (16, 0),   # Late afternoon power-up
]
```

## 🧪 Testing

To ensure your snack reminders are functioning correctly (and deterministically!), run the provided tests:

1.  **Navigate**: Change into the utility's directory:
    ```bash
    cd utils/nightly-snack-dispenser-reminder/
    ```
2.  **Run Tests**: 
    ```bash
    python -m unittest tests/test_reminder.py
    ```
    All tests should pass, confirming the reminder logic works as expected across different times.
