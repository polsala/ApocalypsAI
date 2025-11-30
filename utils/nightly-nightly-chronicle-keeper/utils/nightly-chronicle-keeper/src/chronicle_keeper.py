import argparse
import datetime
import os
import sys

def get_log_directory():
    """Determines the log directory. Creates 'logs/' in the current working directory."""
    log_dir = os.path.join(os.getcwd(), 'logs') # Use current working directory
    
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except OSError as e:
            print(f"Error creating log directory '{log_dir}': {e}", file=sys.stderr)
            # Fallback to current working directory itself if 'logs/' cannot be created
            log_dir = os.getcwd()
            print(f"Falling back to current working directory: '{log_dir}'", file=sys.stderr)
    return log_dir

def main():
    parser = argparse.ArgumentParser(
        description="Append a timestamped entry to your daily chronicle log."
    )
    parser.add_argument(
        "message",
        type=str,
        help="The entry you want to add to your chronicle."
    )

    args = parser.parse_args()

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    log_dir = get_log_directory()
    log_filename = os.path.join(log_dir, f"{date_str}_chronicle.log")

    entry = f"[{time_str}] {args.message}\n"

    try:
        with open(log_filename, "a", encoding="utf-8") as f:
            f.write(entry)
        print(f"Chronicle entry added to '{log_filename}'")
    except IOError as e:
        print(f"Error writing to log file '{log_filename}': {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
