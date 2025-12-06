import argparse
import datetime
import os

def add_entry(message: str, log_file_path: str = "chronicle.md"):
    """
    Adds a timestamped entry to the specified Markdown log file.
    Creates the file if it doesn't exist.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"## {timestamp}\n- {message}\n\n"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_file_path) or '.', exist_ok=True)

    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(entry)
    print(f"Entry added to {log_file_path}")

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Chronicle Keeper: Log timestamped entries."
    )
    parser.add_argument(
        "message",
        type=str,
        help="The message to log."
    )
    parser.add_argument(
        "--file",
        type=str,
        default="chronicle.md",
        help="Path to the log file (default: chronicle.md)."
    )
    args = parser.parse_args()
    add_entry(args.message, args.file)

if __name__ == "__main__":
    main()
