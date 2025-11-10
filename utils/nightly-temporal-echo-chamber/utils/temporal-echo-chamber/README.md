# Temporal Echo Chamber

## Whimsical Purpose
Ever wanted to send a message to your future self, a colleague, or the entire ApocalypsAI community, to be revealed only when the stars align (or a specific date arrives)? The Temporal Echo Chamber is your digital time capsule! Store messages now, and they'll 'echo' back to you at their designated future moment.

## Practical Utility
This utility allows you to schedule messages for future delivery. It's perfect for:
- **Future Reminders**: 'Remember to check the fusion core on 2025-01-01.'
- **Scheduled Announcements**: 'The next nightly integration will include a surprise feature on [date].'
- **Time-Delayed Instructions**: 'If this message is delivered, initiate protocol Omega.'
- **Personal Notes**: A digital diary entry for a future reflection.

## How it Works
Messages are stored locally in a JSON file (`echo_chamber_data.json`) within the utility's directory. A simple Python script handles adding new messages and checking for messages due for delivery.

## Usage

### Prerequisites
- Python 3.8+

### 1. Add a Message to the Chamber
To store a new message, run the `echo_chamber.py` script with the `add` command, providing your message and the desired delivery timestamp.

**Syntax:**
```bash
python src/echo_chamber.py add "Your message here" "YYYY-MM-DD HH:MM:SS"
```

**Example:**
```bash
python src/echo_chamber.py add "Don't forget the self-healing protocols!" "2024-12-25 08:00:00"
```

### 2. Check and Deliver Due Messages
To check if any messages are due for delivery and print them, run the script with the `check` command.

**Syntax:**
```bash
python src/echo_chamber.py check
```

**Example:**
```bash
python src/echo_chamber.py check
```

When messages are delivered, they will be printed to standard output and marked as 'delivered' in the internal data file, preventing re-delivery.

## Data Storage
The utility uses `echo_chamber_data.json` in its root directory to persist messages. This file is automatically created and managed by the script.

## Integration with ApocalypsAI (Example)
You could integrate `python utils/temporal-echo-chamber/src/echo_chamber.py check` into a daily cron job (e.g., via a GitHub Actions workflow) to automatically surface messages when they are due.
