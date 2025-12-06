import os
import argparse
import datetime
import sys

def get_file_info(filepath):
    """Retrieves file modification time and size."""
    try:
        stat = os.stat(filepath)
        return datetime.datetime.fromtimestamp(stat.st_mtime), stat.st_size
    except OSError:
        return None, None

def find_points_of_interest(
    start_path,
    recent_days=None,
    large_kb=None,
    extensions=None,
    max_depth=None
):
    """
    Scavenges the file system for points of interest based on criteria.
    Yields tuples of (filepath, is_recent, is_large, is_matching_ext).
    """
    now = datetime.datetime.now()
    recent_threshold = now - datetime.timedelta(days=recent_days) if recent_days is not None else None
    large_bytes = large_kb * 1024 if large_kb is not None else None

    for root, dirs, files in os.walk(start_path):
        current_depth = root[len(start_path):].count(os.sep)
        if max_depth is not None and current_depth >= max_depth:
            # Prune directories to avoid going deeper than max_depth
            # This modifies 'dirs' in place for the current iteration of os.walk
            dirs[:] = []
            continue

        for name in files:
            filepath = os.path.join(root, name)
            mtime, size = get_file_info(filepath)

            if mtime is None or size is None:
                continue # Skip if file info can't be retrieved

            is_recent = recent_threshold is not None and mtime >= recent_threshold
            is_large = large_bytes is not None and size >= large_bytes
            
            _, ext = os.path.splitext(name)
            is_matching_ext = extensions is None or ext.lstrip('.').lower() in extensions

            if (recent_days is None and large_kb is None and extensions is None) or \
               (is_recent or is_large or is_matching_ext):
                yield filepath, is_recent, is_large, is_matching_ext

def main():
    parser = argparse.ArgumentParser(
        description="Wasteland Wayfinder: A utility for digital scavenging.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="The starting directory for your scavenging expedition. Defaults to current directory."
    )
    parser.add_argument(
        "--recent",
        type=int,
        help="Highlight files modified in the last N days."
    )
    parser.add_argument(
        "--large",
        type=int,
        help="Highlight files larger than N kilobytes."
    )
    parser.add_argument(
        "--ext",
        type=str,
        help="Comma-separated list of file extensions to include (e.g., py,md,txt)."
    )
    parser.add_argument(
        "--depth",
        type=int,
        help="Maximum recursion depth for directory traversal. Default is unlimited."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    extensions_set = {e.strip().lower() for e in args.ext.split(',')} if args.ext else None

    print(f"--- Wasteland Wayfinder: Scavenging '{args.path}' ---")
    found_any = False
    for filepath, is_recent, is_large, is_matching_ext in find_points_of_interest(
        args.path,
        args.recent,
        args.large,
        extensions_set,
        args.depth
    ):
        found_any = True
        tags = []
        if is_recent:
            tags.append("[FRESH TRACKS]")
        if is_large:
            tags.append("[VALUABLE CACHE]")
        if is_matching_ext and extensions_set is not None:
            tags.append("[DATA FRAGMENT]")
        
        tag_str = " ".join(tags)
        if tag_str:
            print(f"  {tag_str} {filepath}")
        else:
            # Only print if no specific filters were applied, or if it matched a filter
            # The find_points_of_interest already handles the "no filters" case
            print(f"  {filepath}")

    if not found_any:
        print("No points of interest found matching your criteria.")
    print("--- Scavenging Complete ---")

if __name__ == "__main__":
    main()
