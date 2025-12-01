# Nightly Snack-pocalypse Reminder

## Description
In the grim darkness of the far future, there is only... hunger. The 'Nightly Snack-pocalypse Reminder' is a crucial utility designed to prevent developer burnout and ensure you're adequately fueled for the ongoing struggle. It periodically reminds you to take a break and grab a snack, keeping your energy levels high and your spirits (relatively) intact.

## How to Use
1.  **Navigate to the utility directory:**
    ```bash
    cd utils/nightly-snack-pocalypse-reminder
    ```
2.  **Install dependencies (if any):**
    This utility uses standard Python libraries, so no special installation is typically required.

3.  **Configure your reminder:**
    Edit `config.json` to set your preferred `interval_minutes` and `reminder_message`.
    ```json
    {
      "interval_minutes": 60,
      "reminder_message": "🚨 Snack-pocalypse Alert! Time to refuel the resistance! 🍪☕"
    }
    ```

4.  **Run the reminder:**
    ```bash
    python src/reminder.py
    ```
    You can run this manually, or set it up as a cron job for regular, automated reminders. For example, to check every 5 minutes:
    ```bash
    */5 * * * * cd /path/to/your/repo/utils/nightly-snack-pocalypse-reminder && python src/reminder.py >> reminder.log 2>&1
    ```

## Configuration (`config.json`)
*   `interval_minutes`: The number of minutes between snack reminders. (Default: 60)
*   `reminder_message`: The message displayed when a snack reminder is triggered. (Default: "🚨 Snack-pocalypse Alert! Time to refuel the resistance! 🍪☕")

## State Management (`state.json`)
The utility maintains a `state.json` file in its directory to track the `last_reminded_timestamp`. This ensures reminders are only triggered after the specified interval has passed. Do not manually edit this file unless you know what you're doing.
