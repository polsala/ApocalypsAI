import argparse
import datetime
import os

def get_log_dir():
    """Returns the path to the chronicles directory."""
    return os.path.join(os.getcwd(), "chronicles")

def get_log_file_path(log_dir, date):
    """Returns the full path for the daily log file."""
    filename = date.strftime("%Y-%m-%d.log")
    return os.path.join(log_dir, filename)

def format_log_entry(message, timestamp):
    """Formats the log entry with a timestamp."""
    return f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {message}\n"

def main():
    parser = argparse.ArgumentParser(
        description="A command-line utility to log daily events with timestamps."
    )
    parser.add_argument(
        "message", type=str, help="The message to be logged in your chronicle."
    )
    args = parser.parse_args()

    now = datetime.datetime.now()
    log_dir = get_log_dir()
    log_file_path = get_log_file_path(log_dir, now)

    # Ensure the log directory exists
    os.makedirs(log_dir, exist_ok=True)

    log_entry = format_log_entry(args.message, now)

    try:
        with open(log_file_path, "a") as f:
            f.write(log_entry)
        print(f"Chronicle entry added to {log_file_path}")
    except IOError as e:
        print(f"Error writing to chronicle file: {e}")
        exit(1)

if __name__ == "__main__":
    main()
