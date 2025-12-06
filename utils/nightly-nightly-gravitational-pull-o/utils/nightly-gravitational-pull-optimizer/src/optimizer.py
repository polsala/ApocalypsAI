import os
import sys
import argparse

def get_human_readable_size(size_bytes):
    """Convert bytes to a human-readable string (e.g., KB, MB, GB)."""
    if size_bytes is None:
        return "N/A"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def scan_directory(path, threshold_mb):
    """Scans a directory for large files and aggregates directory sizes.

    Args:
        path (str): The root directory to scan.
        threshold_mb (float): The minimum size in MB for items to be reported.

    Returns:
        list: A list of tuples (size_bytes, type, path) for heavy components.
    """
    threshold_bytes = threshold_mb * 1024 * 1024
    final_heavy_components = []

    print(f"Scanning directory: {path}")

    # First, collect all file sizes
    file_info = [] # List of (size, path)
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                file_info.append((size, file_path))
            except OSError:
                pass # Silently skip unreadable files/symlinks for robustness
    
    # Calculate total size for each directory including its contents
    # This requires iterating from deepest to shallowest directories (topdown=False)
    dir_total_sizes = {}
    for root, dirs, files in os.walk(path, topdown=False): 
        current_dir_total_size = 0
        for file in files:
            file_path = os.path.join(root, file)
            try:
                current_dir_total_size += os.path.getsize(file_path)
            except OSError:
                pass
        for d in dirs:
            sub_dir_path = os.path.join(root, d)
            current_dir_total_size += dir_total_sizes.get(sub_dir_path, 0)
        dir_total_sizes[root] = current_dir_total_size

    # Collect heavy files
    for size, file_path in file_info:
        if size >= threshold_bytes:
            final_heavy_components.append((size, 'FILE', file_path))
    
    # Collect heavy directories
    # We report a directory if its total size (including children) exceeds the threshold.
    # We exclude the root path itself from being reported as a 'heavy directory' to focus on sub-components.
    for d_path, d_size in dir_total_sizes.items():
        if d_size >= threshold_bytes and d_path != path:
            final_heavy_components.append((d_size, 'DIR', d_path))

    # Sort by size in descending order
    final_heavy_components.sort(key=lambda x: x[0], reverse=True)

    # Remove duplicates based on path, keeping the first occurrence (which is the largest due to sorting)
    unique_components = []
    seen_paths = set()
    for size, item_type, item_path in final_heavy_components:
        if item_path not in seen_paths:
            unique_components.append((size, item_type, item_path))
            seen_paths.add(item_path)

    return unique_components

def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory for large files and directories."
    )
    parser.add_argument(
        "path", 
        nargs="?", 
        default=".", 
        help="The directory to scan. Defaults to current working directory."
    )
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=10.0, 
        help="Minimum size in MB for an item to be reported. Defaults to 10.0 MB."
    )

    args = parser.parse_args()

    scan_path = os.path.abspath(args.path)
    threshold_mb = args.threshold

    if not os.path.isdir(scan_path):
        print(f"Error: Path '{scan_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    heavy_components = scan_directory(scan_path, threshold_mb)

    print(f"\nHeavy Components (Threshold: {threshold_mb:.2f} MB):")
    print("----------------------------------------")
    if not heavy_components:
        print("No heavy components found above the threshold.")
    else:
        for size, item_type, item_path in heavy_components:
            print(f"[{item_type}] {get_human_readable_size(size)}: {item_path}")
    print("----------------------------------------")
    print(f"Total heavy components found: {len(heavy_components)}")

if __name__ == "__main__":
    main()
