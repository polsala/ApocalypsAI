import os
import re
import argparse
import datetime
import json
from typing import List, Dict, Any

def get_file_metadata(filepath: str) -> Dict[str, Any]:
    """Retrieves metadata for a given file."""
    stat = os.stat(filepath)
    return {
        "path": filepath,
        "name": os.path.basename(filepath),
        "size": stat.st_size,
        "modified_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created_at": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
    }

def scavenge_files(
    directory: str,
    pattern: str = None,
    min_size: int = None,
    max_size: int = None,
    max_age_days: int = None,
) -> List[Dict[str, Any]]:
    """
    Scavenges files in a directory based on specified criteria.

    Args:
        directory: The root directory to search.
        pattern: A regex pattern to match against file names.
        min_size: Minimum file size in bytes.
        max_size: Maximum file size in bytes.
        max_age_days: Only include files modified within the last N days.

    Returns:
        A list of dictionaries, each containing file metadata for matching files.
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    matching_files = []
    regex = re.compile(pattern) if pattern else None
    now = datetime.datetime.now()

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                metadata = get_file_metadata(filepath)

                # Apply pattern filter
                if regex and not regex.search(filename):
                    continue

                # Apply size filters
                if min_size is not None and metadata["size"] < min_size:
                    continue
                if max_size is not None and metadata["size"] > max_size:
                    continue

                # Apply age filter
                if max_age_days is not None:
                    modified_dt = datetime.datetime.fromisoformat(metadata["modified_at"])
                    age_delta = now - modified_dt
                    if age_delta.days > max_age_days:
                        continue

                matching_files.append(metadata)
            except OSError:
                # Ignore files we can't access (e.g., permission errors, broken symlinks)
                continue

    # Prioritize: newer and larger files first (more "valuable" stardust)
    matching_files.sort(key=lambda x: (x["modified_at"], x["size"]), reverse=True)
    return matching_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Stardust Scavenger Searcher: Unearthing Digital Relics."
    )
    parser.add_argument(
        "--directory",
        "-d",
        required=True,
        help="The root directory to begin the scavenger hunt.",
    )
    parser.add_argument(
        "--pattern",
        "-p",
        help="A regular expression to match against file names (e.g., '.*\\.log$').",
    )
    parser.add_argument(
        "--min-size",
        "-smin",
        type=int,
        help="Minimum file size in bytes.",
    )
    parser.add_argument(
        "--max-size",
        "-smax",
        type=int,
        help="Maximum file size in bytes.",
    )
    parser.add_argument(
        "--max-age-days",
        "-a",
        type=int,
        help="Only include files modified within the last N days.",
    )
    parser.add_argument(
        "--output-format",
        "-o",
        choices=["text", "json"],
        default="text",
        help="Output format: 'text' (default) or 'json'.",
    )

    args = parser.parse_args()

    try:
        results = scavenge_files(
            directory=args.directory,
            pattern=args.pattern,
            min_size=args.min_size,
            max_size=args.max_size,
            max_age_days=args.max_age_days,
        )

        if args.output_format == "json":
            print(json.dumps(results, indent=2))
        else:
            if not results:
                print("No digital relics found matching your criteria. Keep scavenging!")
            else:
                print(f"Found {len(results)} digital relics:")
                for i, file_data in enumerate(results):
                    print(f"--- Relic {i+1} ---")
                    print(f"  Path: {file_data['path']}")
                    print(f"  Name: {file_data['name']}")
                    print(f"  Size: {file_data['size']} bytes")
                    print(f"  Modified: {file_data['modified_at']}")
                    print("-" * 20)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=os.sys.stderr)
        os.sys.exit(1)
    except Exception as e:
        print(f"An unexpected anomaly occurred: {e}", file=os.sys.stderr)
        os.sys.exit(1)

if __name__ == "__main__":
    main()
