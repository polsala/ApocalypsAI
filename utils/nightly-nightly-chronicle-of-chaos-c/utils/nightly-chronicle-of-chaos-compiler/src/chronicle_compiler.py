import argparse
import os
import datetime

LOGS_DIR = "logs"
CHRONICLE_FILE = "chronicle.md"

def _get_log_filepath(date: datetime.date) -> str:
    """Returns the full path for a daily log file."""
    return os.path.join(LOGS_DIR, date.strftime("%Y-%m-%d.log"))

def add_entry(entry_text: str):
    """Adds a new timestamped entry to the current day's log file."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    today = datetime.date.today()
    log_filepath = _get_log_filepath(today)
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    with open(log_filepath, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {entry_text}\n")
    print(f"Entry added to {log_filepath}")

def compile_chronicle():
    """Compiles all daily log files into a single chronicle.md file."""
    if not os.path.exists(LOGS_DIR):
        print(f"No '{LOGS_DIR}' directory found. Nothing to compile.")
        return

    log_files = sorted([
        f for f in os.listdir(LOGS_DIR)
        if f.endswith('.log') and os.path.isfile(os.path.join(LOGS_DIR, f))
    ])

    if not log_files:
        print(f"No log files found in '{LOGS_DIR}'. Nothing to compile.")
        return

    compiled_content = []
    for filename in log_files:
        date_str = filename.replace('.log', '')
        try:
            log_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(f"Skipping malformed log file: {filename}")
            continue

        filepath = os.path.join(LOGS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        compiled_content.append(f"## {log_date.strftime('%Y-%m-%d')}\n\n{content.strip()}\n\n")

    with open(CHRONICLE_FILE, "w", encoding="utf-8") as f:
        f.write("# Chronicle of Chaos\n\n")
        f.write("\n".join(compiled_content))
    print(f"Chronicle compiled to {CHRONICLE_FILE}")

def view_log(log_type: str):
    """Views the content of the current day's log or the compiled chronicle."""
    if log_type == "daily":
        today = datetime.date.today()
        log_filepath = _get_log_filepath(today)
        if os.path.exists(log_filepath):
            with open(log_filepath, "r", encoding="utf-8") as f:
                print(f"\n--- Daily Log ({today.strftime('%Y-%m-%d')}) ---\n")
                print(f.read())
                print("------------------------------------\n")
        else:
            print(f"No log entries for today ({today.strftime('%Y-%m-%d')}).")
    elif log_type == "chronicle":
        if os.path.exists(CHRONICLE_FILE):
            with open(CHRONICLE_FILE, "r", encoding="utf-8") as f:
                print(f"\n--- Compiled Chronicle ---\n")
                print(f.read())
                print("--------------------------\n")
        else:
            print(f"No compiled chronicle found. Run 'compile' first.")
    else:
        print("Invalid view type. Use 'daily' or 'chronicle'.")

def main():
    parser = argparse.ArgumentParser(
        description="A utility to compile daily log entries into a single chronicle."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new entry to today's log.")
    add_parser.add_argument("entry", type=str, help="The text of the log entry.")

    compile_parser = subparsers.add_parser("compile", help="Compile all daily logs into a single chronicle.")

    view_parser = subparsers.add_parser("view", help="View a specific log.")
    view_parser.add_argument("type", choices=["daily", "chronicle"], help="Type of log to view ('daily' or 'chronicle').")

    args = parser.parse_args()

    if args.command == "add":
        add_entry(args.entry)
    elif args.command == "compile":
        compile_chronicle()
    elif args.command == "view":
        view_log(args.type)

if __name__ == "__main__":
    main()
