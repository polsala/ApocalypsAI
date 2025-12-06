# Nightly Hydration & Sustenance Reminder

A crucial utility for the diligent survivors of the codebase apocalypse! This tool ensures you don't succumb to dehydration or hunger while battling bugs and deploying features. It periodically reminds you to take a break, hydrate, and refuel your organic processing unit.

## Purpose

In the relentless pursuit of code perfection, it's easy to forget basic human needs. This utility acts as your personal, apocalypse-themed wellness guardian, gently nudging you to step away, drink some water, and grab a snack.

## How it Works

When executed, the `reminder.py` script checks a timestamp file (`last_reminded.txt`) in its directory. If enough time (default: 2 hours) has passed since the last reminder, it prints a whimsical message to your console, encouraging you to hydrate or refuel, and then updates the timestamp. If not enough time has passed, it silently exits.

This utility is designed to be run periodically, for example, via a cron job or a scheduled task, to provide regular, non-intrusive reminders throughout your coding sessions.

## Usage

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-hydration-sustenance-reminder/src
    ```
2.  **Run the reminder**:
    ```bash
    python reminder.py
    ```

### Configuration

The reminder interval and messages are currently hardcoded within `src/reminder.py`. Future enhancements might include external configuration.

## Example Output

```
[ApocalypsAI Wellness Protocol] Warning: Your organic processing unit requires hydration! Seek water before your code turns to dust.
```
```
