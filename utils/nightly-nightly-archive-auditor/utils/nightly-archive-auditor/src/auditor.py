import os
import datetime
import argparse

def find_stale_files(directory, age_days):
    """
    Scans a directory for files not modified within the last `age_days`.
    Returns a list of (filepath, last_modified_timestamp) for stale files.
    """
    stale_files = []
    now = datetime.datetime.now()
    threshold_date = now - datetime.timedelta(days=age_days)

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                # Get modification time as a datetime object
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_datetime = datetime.datetime.fromtimestamp(mtime_timestamp)

                if mtime_datetime < threshold_date:
                    stale_files.append((filepath, mtime_datetime))
            except OSError:
                # Handle cases where file might be inaccessible or deleted during scan
                pass
    return stale_files

def generate_report(stale_files, directory, age_days):
    """
    Generates a Markdown report of stale files.
    """
    report_lines = [
        f"# Apocalypse Archive Auditor Report for '{directory}'",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"---",
        f"This report identifies files not modified in the last **{age_days} days**.",
        f"",
    ]

    if not stale_files:
        report_lines.append("No stale files found. Your archives are surprisingly fresh!")
    else:
        report_lines.append(f"Found {len(stale_files)} potentially stale files:")
        report_lines.append("")
        report_lines.append("| File Path | Last Modified | Age (days) |")
        report_lines.append("| :-------- | :------------ | :--------- |")

        stale_files.sort(key=lambda x: x[1]) # Sort by oldest first

        for filepath, mtime_datetime in stale_files:
            age_delta = datetime.datetime.now() - mtime_datetime
            report_lines.append(
                f"| `{filepath}` | {mtime_datetime.strftime('%Y-%m-%d')} | {age_delta.days} |"
            )
    return "\n".join(report_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Apocalypse Archive Auditor: Scans a directory for files not modified within a specified period."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The directory to scan for stale files."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=365,
        help="Number of days after which a file is considered stale (default: 365 days)."
    )
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found or is not a directory.", file=os.sys.stderr)
        os.sys.exit(1)

    print(f"Scanning '{args.directory}' for files older than {args.age} days...")
    stale_files = find_stale_files(args.directory, args.age)
    report = generate_report(stale_files, args.directory, args.age)
    print(report)

if __name__ == "__main__":
    main()
