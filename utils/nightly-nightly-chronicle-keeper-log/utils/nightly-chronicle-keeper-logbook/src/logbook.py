import argparse
import datetime
import os

def get_log_entry(message: str) -> str:
    """Generates a timestamped log entry."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"### {timestamp}\n{message}\n"

def get_log_filename(base_filename: str, daily: bool) -> str:
    """Determines the log file name based on daily flag."""
    if daily:
        date_prefix = datetime.datetime.now().strftime("%Y-%m-%d")
        name, ext = os.path.splitext(base_filename)
        return f"{date_prefix}_{name}{ext}"
    return base_filename

def ensure_log_directory_exists(filepath: str):
    """Ensures the directory for the log file exists."""
    log_dir = os.path.dirname(filepath)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chronicle Keeper Logbook: Record timestamped entries."
    )
    parser.add_argument(
        "-m", "--message",
        type=str,
        required=True,
        help="The message to log."
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        default="chronicle.md",
        help="The base name of the log file (e.g., 'chronicle.md')."
    )
    parser.add_argument(
        "--daily",
        action="store_true",
        help="Use a daily log file (e.g., 'YYYY-MM-DD_chronicle.md')."
    )

    args = parser.parse_args()

    log_filename = get_log_filename(args.file, args.daily)
    log_entry = get_log_entry(args.message)

    # Determine the base directory for logs.
    # This places logs in a 'logs' folder at the root of the utility,
    # e.g., utils/nightly-chronicle-keeper-logbook/logs/
    utility_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_base_dir = os.path.join(utility_root_dir, "logs")
    full_log_filepath = os.path.join(log_base_dir, log_filename)

    ensure_log_directory_exists(full_log_filepath)

    try:
        with open(full_log_filepath, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n") # Add an extra newline for separation between entries
        print(f"Entry logged to {full_log_filepath}")
    except IOError as e:
        print(f"Error writing to log file {full_log_filepath}: {e}", file=os.stderr)
        exit(1)

if __name__ == "__main__":
    main()
