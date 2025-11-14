import os
import re
import datetime
import argparse

def find_dust_bunnies(
    directory_path: str,
    age_days: int,
    patterns: list[str]
) -> list[dict]:
    """
    Scans a directory for files that are considered 'digital dust bunnies'.

    A file is a 'dust bunny' if:
    1. It's older than `age_days`.
    2. Its filename matches any of the provided `patterns`.

    Args:
        directory_path: The path to the directory to scan.
        age_days: The age threshold in days. Files older than this are flagged.
        patterns: A list of regular expression strings to match against filenames.

    Returns:
        A list of dictionaries, each representing a found dust bunny with its path,
        reason, and last modified date.
    """
    dust_bunnies = []
    current_time = datetime.datetime.now()
    age_threshold = datetime.timedelta(days=age_days)

    compiled_patterns = [re.compile(p) for p in patterns]

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            is_dust_bunny = False
            reasons_set = set()
            last_modified_dt = None

            try:
                # Check age
                mtime_timestamp = os.path.getmtime(file_path)
                last_modified_dt = datetime.datetime.fromtimestamp(mtime_timestamp)
                if (current_time - last_modified_dt) > age_threshold:
                    is_dust_bunny = True
                    reasons_set.add(f"Older than {age_days} days")

                # Check patterns
                for pattern in compiled_patterns:
                    if pattern.search(file_name):
                        is_dust_bunny = True
                        reasons_set.add(f"Matches pattern: {pattern.pattern}")
                        # No break here, a file can match multiple patterns, all should be reported

                if is_dust_bunny:
                    dust_bunnies.append({
                        "path": file_path,
                        "reason": "; ".join(sorted(list(reasons_set))), # Sort for deterministic output
                        "last_modified": last_modified_dt.strftime("%Y-%m-%d") if last_modified_dt else "N/A"
                    })
            except OSError as e:
                # Handle cases where file might be inaccessible or disappear during scan
                print(f"Warning: Could not access {file_path} - {e}")
                continue

    return dust_bunnies

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for 'digital dust bunnies' (old or temporary files)."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The directory path to scan."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=365,
        help="Files older than this many days will be flagged. Default: 365."
    )
    parser.add_argument(
        "--patterns",
        nargs='*',
        default=["\\.tmp$", "\\.bak$", "~$", "\\.log$", "\\.swp$", "^#.*#$", "\.DS_Store$", "Thumbs\.db$"], # Common temp/backup/OS patterns
        help="Regular expression patterns to match against filenames. Files matching any pattern will be flagged. Default: common temp/backup patterns."
    )

    args = parser.parse_args()

    print(f"Scanning {args.path} for digital dust bunnies...")

    found_bunnies = find_dust_bunnies(args.path, args.age, args.patterns)

    if found_bunnies:
        print(f"\nFound {len(found_bunnies)} digital dust bunnies:\n")
        for bunny in found_bunnies:
            print(f"- {bunny['path']} (Reason: {bunny['reason']}, Last modified: {bunny['last_modified']})")
        print("\nConsider reviewing these files for potential cleanup.")
    else:
        print("\nNo digital dust bunnies found. Your directory is sparkling clean!")

if __name__ == "__main__":
    main()
