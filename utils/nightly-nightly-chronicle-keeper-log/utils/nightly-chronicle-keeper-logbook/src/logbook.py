import argparse
import datetime
import os

def _get_timestamp():
    """Returns a formatted timestamp."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_entry(message: str, log_file_path: str):
    """
    Appends a timestamped message to the specified log file.
    Creates the directory if it doesn't exist.
    """
    log_dir = os.path.dirname(log_file_path)
    # Only try to create directory if log_file_path includes a directory component
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    with open(log_file_path, 'a', encoding='utf-8') as f:
        f.write(f"[{_get_timestamp()}] {message}\n")
    print(f"Entry added to {log_file_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Chronicle-Keeper Logbook: Document your journey through the apocalypse."
    )
    parser.add_argument(
        "message",
        type=str,
        help="The message to add to your chronicle."
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=os.path.join("logs", "chronicle.log"),
        help="Path to the chronicle log file. Defaults to 'logs/chronicle.log'."
    )
    
    args = parser.parse_args()
    add_entry(args.message, args.output)

if __name__ == "__main__":
    main()
