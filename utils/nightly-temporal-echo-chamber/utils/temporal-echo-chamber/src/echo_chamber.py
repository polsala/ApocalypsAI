import json
import os
import sys
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'echo_chamber_data.json')

def _load_messages():
    """Loads messages from the data file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: {DATA_FILE} is corrupted. Starting with an empty chamber.", file=sys.stderr)
        return []

def _save_messages(messages):
    """Saves messages to the data file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f, indent=4)

def add_message(message_content: str, delivery_time_str: str):
    """Adds a new message to the chamber.

    Args:
        message_content: The content of the message.
        delivery_time_str: The target delivery time in 'YYYY-MM-DD HH:MM:SS' format.
    """
    try:
        delivery_dt = datetime.strptime(delivery_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print(f"Error: Invalid time format. Please use 'YYYY-MM-DD HH:MM:SS'. Got: {delivery_time_str}", file=sys.stderr)
        sys.exit(1)

    messages = _load_messages()
    messages.append({
        'message': message_content,
        'delivery_time': delivery_dt.isoformat(),
        'delivered': False
    })
    _save_messages(messages)
    print(f"Message scheduled for delivery on {delivery_time_str}.")

def check_and_deliver_messages():
    """Checks for and delivers messages that are due.

    Delivered messages are printed to stdout and marked as delivered.
    """
    messages = _load_messages()
    current_time = datetime.now()
    delivered_count = 0

    for msg in messages:
        if not msg['delivered']:
            delivery_dt = datetime.fromisoformat(msg['delivery_time'])
            if current_time >= delivery_dt:
                print(f"[Temporal Echo Chamber - Delivered] {msg['message']} (Scheduled: {msg['delivery_time']})")
                msg['delivered'] = True
                delivered_count += 1
    
    if delivered_count > 0:
        _save_messages(messages)
        print(f"\n{delivered_count} message(s) delivered.")
    else:
        print("No messages due for delivery at this time.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/echo_chamber.py <command> [args]", file=sys.stderr)
        print("Commands:", file=sys.stderr)
        print("  add \"<message>\" \"YYYY-MM-DD HH:MM:SS\"", file=sys.stderr)
        print("  check", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) != 4:
            print("Usage: python src/echo_chamber.py add \"<message>\" \"YYYY-MM-DD HH:MM:SS\"", file=sys.stderr)
            sys.exit(1)
        message_content = sys.argv[2]
        delivery_time_str = sys.argv[3]
        add_message(message_content, delivery_time_str)
    elif command == 'check':
        if len(sys.argv) != 2:
            print("Usage: python src/echo_chamber.py check", file=sys.stderr)
            sys.exit(1)
        check_and_deliver_messages()
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
