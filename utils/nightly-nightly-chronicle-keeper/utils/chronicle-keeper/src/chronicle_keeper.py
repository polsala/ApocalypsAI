import argparse
import datetime
import os

def append_to_logbook(message: str, log_file: str = "logbook.md"):
    """
    Appends a timestamped message to the logbook file.
    Creates the file if it doesn't exist.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"## {timestamp}\n\n{message}\n\n---\n\n"

    mode = 'a' if os.path.exists(log_file) else 'w'
    with open(log_file, mode, encoding='utf-8') as f:
        f.write(entry)
    print(f"Entry added to {log_file}.")

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Chronicle Keeper: Log your daily findings and thoughts."
    )
    parser.add_argument(
        "message",
        type=str,
        help="The message to append to your chronicle logbook."
    )
    parser.add_argument(
        "--file",
        type=str,
        default="logbook.md",
        help="The logbook file to write to (default: logbook.md)."
    )
    args = parser.parse_args()
    append_to_logbook(args.message, args.file)

if __name__ == "__main__":
    main()
