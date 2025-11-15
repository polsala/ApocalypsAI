import os
import datetime
import argparse
import json
import sys

def scan_directory(path, age_threshold_dt):
    """
    Scans the given path recursively for files older than age_threshold_dt.
    Returns a list of (filepath, modified_datetime) tuples for debris files.
    """
    debris_files = []
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.", file=sys.stderr)
        return []

    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_dt = datetime.datetime.fromtimestamp(mtime_timestamp)
                if mtime_dt < age_threshold_dt:
                    debris_files.append((filepath, mtime_dt))
            except OSError as e:
                print(f"Warning: Could not access file '{filepath}': {e}", file=sys.stderr)
                continue
    return debris_files

def generate_report(scan_path, age_days, debris_files, report_format):
    """
    Generates and prints a report of debris files in the specified format.
    """
    current_time = datetime.datetime.now()

    if report_format == 'json':
        json_output = {
            "scan_path": scan_path,
            "age_threshold_days": age_days,
            "report_generated": current_time.isoformat(),
            "debris_files": [
                {
                    "path": filepath,
                    "modified_timestamp": mtime_dt.timestamp(),
                    "modified_datetime": mtime_dt.isoformat()
                }
                for filepath, mtime_dt in debris_files
            ]
        }
        print(json.dumps(json_output, indent=2))
    else: # text format
        print(f"Data Debris Report for: {scan_path} (Older than {age_days} days)")
        print("-" * (len(scan_path) + 40))
        if not debris_files:
            print("No data debris found. Your digital landscape is pristine!")
        else:
            print(f"Found {len(debris_files)} debris files:\n")
            for filepath, mtime_dt in debris_files:
                print(f"- {filepath} (Modified: {mtime_dt.strftime('%Y-%m-%d %H:%M:%S')})")
            print("\nConsider reviewing these files for archiving or deletion.")

def main():
    parser = argparse.ArgumentParser(
        description="Scan directories for old, unused files (data debris) and generate a report."
    )
    parser.add_argument(
        "path",
        type=str,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--age-days",
        type=int,
        default=30,
        help="The minimum age in days for a file to be considered 'debris'. Defaults to 30."
    )
    parser.add_argument(
        "--report-format",
        type=str,
        choices=['text', 'json'],
        default='text',
        help="The format of the output report. Can be 'text' or 'json'. Defaults to 'text'."
    )

    args = parser.parse_args()

    if args.age_days < 0:
        print("Error: --age-days cannot be negative.", file=sys.stderr)
        sys.exit(1)

    current_time = datetime.datetime.now()
    age_threshold_dt = current_time - datetime.timedelta(days=args.age_days)

    debris_files = scan_directory(args.path, age_threshold_dt)
    if debris_files is None: # Error occurred in scan_directory
        sys.exit(1)

    generate_report(args.path, args.age_days, debris_files, args.report_format)

if __name__ == "__main__":
    main()
