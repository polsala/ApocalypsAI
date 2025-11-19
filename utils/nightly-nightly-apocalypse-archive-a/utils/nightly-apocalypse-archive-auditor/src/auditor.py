import os
import datetime
from collections import defaultdict

def audit_archive(directory_path: str, include_extensions: list[str] = None, age_threshold_years: int = 5) -> dict:
    """
    Scans a directory for files, categorizes them by extension, and identifies old files.

    Args:
        directory_path: The path to the directory to audit.
        include_extensions: A list of file extensions (e.g., ['.txt', '.md']) to include.
                            If None or empty, all files are included.
        age_threshold_years: Files older than this threshold will be flagged as 'old'.

    Returns:
        A dictionary containing the audit report.
    """
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    report = {
        "total_files": 0,
        "total_size_bytes": 0,
        "files_by_extension": defaultdict(int),
        "old_files": [],
        "summary": ""
    }

    current_time = datetime.datetime.now()
    age_threshold_seconds = age_threshold_years * 365.25 * 24 * 60 * 60 # Approximate seconds in years

    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            _, ext = os.path.splitext(file_name)
            ext = ext.lower() # Normalize extension

            if include_extensions and ext not in include_extensions:
                continue

            try:
                file_size = os.path.getsize(file_path)
                file_mtime_timestamp = os.path.getmtime(file_path)
                file_mtime = datetime.datetime.fromtimestamp(file_mtime_timestamp)

                report["total_files"] += 1
                report["total_size_bytes"] += file_size
                report["files_by_extension"][ext] += 1

                age_seconds = (current_time - file_mtime).total_seconds()
                if age_seconds > age_threshold_seconds:
                    age_years = age_seconds / (365.25 * 24 * 60 * 60)
                    report["old_files"].append({
                        "path": file_path,
                        "age_years": round(age_years, 1),
                        "last_modified": file_mtime.isoformat()
                    })
            except OSError as e:
                # Handle cases where file might be inaccessible or deleted during scan
                print(f"Warning: Could not process file {file_path}: {e}")
                continue

    report["summary"] = (
        f"Audit complete for '{directory_path}':\n"
        f"  Total files: {report['total_files']}\n"
        f"  Total size: {report['total_size_bytes'] / (1024*1024):.2f} MB\n"
        f"  Files by extension: {dict(report['files_by_extension'])}\n"
        f"  Old files (>{age_threshold_years} years): {len(report['old_files'])}"
    )
    return report

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Apocalypse Archive Auditor: Scans a directory for files and generates a report."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory to audit."
    )
    parser.add_argument(
        "--extensions",
        nargs='*',
        default=[],
        help="List of file extensions to include (e.g., .txt .md). If empty, all files are included."
    )
    parser.add_argument(
        "--age-threshold",
        type=int,
        default=5,
        help="Files older than this many years will be flagged as 'old'. Default is 5."
    )

    args = parser.parse_args()

    # Normalize extensions to include leading dot if missing
    normalized_extensions = [ext if ext.startswith('.') else '.' + ext for ext in args.extensions]

    try:
        report = audit_archive(args.directory, normalized_extensions, args.age_threshold)
        print(report["summary"])
        if report["old_files"]:
            print("\n--- Old Files Details ---")
            for f in report["old_files"]:
                print(f"  - Path: {f['path']}, Age: {f['age_years']} years, Last Modified: {f['last_modified']}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
