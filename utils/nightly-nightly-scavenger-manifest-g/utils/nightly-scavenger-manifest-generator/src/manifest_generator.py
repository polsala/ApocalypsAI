import os
import json
import argparse
from datetime import datetime, timedelta

def generate_manifest(directory_path: str, recent_days: int = None) -> dict:
    """
    Scans a directory, categorizes files by extension, and generates a summary manifest.

    Args:
        directory_path: The path to the directory to scan.
        recent_days: Optional. If provided, lists files modified within this many days.

    Returns:
        A dictionary containing the manifest data.
    """
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    manifest = {
        "scanned_directory": os.path.abspath(directory_path),
        "total_files": 0,
        "total_size_bytes": 0,
        "summary_by_extension": {},
        "recent_files": []
    }

    now = datetime.now()
    recent_threshold = now - timedelta(days=recent_days) if recent_days is not None else None

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                file_size = os.path.getsize(file_path)
                mod_timestamp = os.path.getmtime(file_path)
                mod_datetime = datetime.fromtimestamp(mod_timestamp)

                manifest["total_files"] += 1
                manifest["total_size_bytes"] += file_size

                _, ext = os.path.splitext(file_name)
                ext = ext.lower() if ext else "no_extension"

                if ext not in manifest["summary_by_extension"]:
                    manifest["summary_by_extension"][ext] = {"count": 0, "total_size_bytes": 0}
                manifest["summary_by_extension"][ext]["count"] += 1
                manifest["summary_by_extension"][ext]["total_size_bytes"] += file_size

                if recent_threshold is not None and mod_datetime >= recent_threshold:
                    manifest["recent_files"].append({
                        "path": os.path.abspath(file_path),
                        "size_bytes": file_size,
                        "modified_timestamp": mod_timestamp
                    })
            except OSError:
                # Ignore files that cannot be accessed (e.g., permission errors, broken symlinks)
                pass

    # Sort recent files by modification time, newest first
    manifest["recent_files"].sort(key=lambda x: x["modified_timestamp"], reverse=True)

    return manifest

def main():
    parser = argparse.ArgumentParser(
        description="Generate a manifest of files in a directory, categorized by extension."
    )
    parser.add_argument(
        "directory_path",
        type=str,
        help="The path to the directory to scan."
    )
    parser.add_argument(
        "--recent-days",
        type=int,
        help="Optional. Number of days back to consider a file 'recent'."
    )

    args = parser.parse_args()

    try:
        manifest = generate_manifest(args.directory_path, args.recent_days)
        print(json.dumps(manifest, indent=4))
    except FileNotFoundError as e:
        print(json.dumps({"error": str(e)}), indent=4)
        exit(1)
    except Exception as e:
        print(json.dumps({"error": f"An unexpected error occurred: {e}"}), indent=4)
        exit(1)

if __name__ == "__main__":
    main()
