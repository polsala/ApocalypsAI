import os
import time
import datetime
import argparse
from collections import defaultdict

def get_file_age_category(mtime_timestamp, now_dt):
    """
    Determines the age category of a file based on its modification timestamp.

    Args:
        mtime_timestamp (float): The modification time of the file as a Unix timestamp.
        now_dt (datetime.datetime): The current datetime object for comparison.

    Returns:
        tuple: A tuple containing (category_name, emoji, days_ago).
    """
    mtime_dt = datetime.datetime.fromtimestamp(mtime_timestamp)
    age_delta = now_dt - mtime_dt
    days_ago = age_delta.days

    if days_ago <= 7:
        return "Blooming", "🌷", days_ago
    elif days_ago <= 30:
        return "Thriving", "🌱", days_ago
    elif days_ago <= 90:
        return "Wilting", "🍂", days_ago
    else:
        return "Fossilized", "💀", days_ago

def scan_directory(path, now_dt=None):
    """
    Scans a directory and categorizes files by their modification age.

    Args:
        path (str): The root directory to scan.
        now_dt (datetime.datetime, optional): The current datetime.
                                              Used for deterministic testing.
                                              Defaults to datetime.datetime.now().

    Returns:
        dict: A dictionary where keys are categories and values are lists of
              (filepath, emoji, days_ago) tuples.
    """
    if now_dt is None:
        now_dt = datetime.datetime.now()

    if not os.path.isdir(path):
        raise FileNotFoundError(f"Directory not found: {path}")

    categorized_files = defaultdict(list)
    total_files = 0

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(file_path)
                category, emoji, days_ago = get_file_age_category(mtime, now_dt)
                categorized_files[category].append((file_path, emoji, days_ago))
                total_files += 1
            except OSError:
                # Ignore files that might be inaccessible or have issues
                continue
    return dict(categorized_files), total_files

def main():
    parser = argparse.ArgumentParser(
        description="Monitor your digital garden for file freshness."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to scan."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show individual files in the report, not just summaries."
    )
    args = parser.parse_args()

    try:
        categorized_files, total_files = scan_directory(args.path)

        print(f"Digital Garden Report for {args.path}:\n")

        # Define order for categories
        category_order = ["Blooming", "Thriving", "Wilting", "Fossilized"]
        category_emojis = {
            "Blooming": "🌷",
            "Thriving": "🌱",
            "Wilting": "🍂",
            "Fossilized": "💀"
        }
        category_descriptions = {
            "Blooming": "last 7 days",
            "Thriving": "last 30 days",
            "Wilting": "last 90 days",
            "Fossilized": "over 90 days"
        }

        for category in category_order:
            emoji = category_emojis.get(category, "")
            description = category_descriptions.get(category, "")
            files_in_category = categorized_files.get(category, [])
            count = len(files_in_category)

            print(f"{emoji} {category} ({description}): {count} files")
            if args.verbose and count > 0:
                for file_path, _, days_ago in sorted(files_in_category, key=lambda x: x[2]):
                    # Make path relative to the scanned directory for cleaner output
                    relative_path = os.path.relpath(file_path, args.path)
                    print(f"  - {relative_path} ({days_ago} days ago)")
                print() # Add a newline for better readability between categories

        print(f"\nTotal files scanned: {total_files}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
