import argparse
import datetime
import os

def add_log_entry(message: str, log_file: str = "chronicle.md") -> int:
    """
    Appends a timestamped message to the specified log file.
    Creates the file if it does not exist.
    Returns 0 on success, 1 on error.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"### {timestamp}\n{message}\n\n"

    try:
        with open(log_file, 'a') as f:
            f.write(entry)
        print(f"Entry added to {log_file}")
    except IOError as e:
        print(f"Error writing to log file {log_file}: {e}")
        return 1
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Append a timestamped entry to a chronicle log file."
    )
    parser.add_argument(
        "message",
        type=str,
        help="The message to add to the chronicle."
    )
    parser.add_argument(
        "--file",
        type=str,
        default="chronicle.md",
        help="The name of the log file (default: chronicle.md)."
    )
    args = parser.parse_args()
    exit_code = add_log_entry(args.message, args.file)
    exit(exit_code)

if __name__ == "__main__":
    main()
