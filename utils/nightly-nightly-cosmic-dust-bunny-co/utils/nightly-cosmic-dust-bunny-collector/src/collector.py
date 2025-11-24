import os
import sys
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """
    Calculates the age of a file in days.
    # Mock rationale: os.path.getmtime returns a timestamp, which depends on the current time.
    # Mocking this allows deterministic testing of age-based filtering.
    """
    mtime = os.path.getmtime(filepath)
    file_datetime = datetime.fromtimestamp(mtime)
    return (datetime.now() - file_datetime).days

def is_empty_dir(path):
    """
    Checks if a directory is empty.
    # Mock rationale: os.listdir depends on the actual file system state.
    # Mocking this allows deterministic testing of empty directory detection.
    """
    return not os.listdir(path)

def collect_dust_bunnies(paths, age_threshold_days, extensions, report_empty_dirs):
    """
    Scans specified paths for old files, specific extensions, and empty directories.
    """
    dust_bunnies = {
        "old_files": [],
        "extension_files": [],
        "empty_directories": []
    }

    for path in paths:
        if not os.path.exists(path):
            print(f"Warning: Path not found - {path}", file=sys.stderr)
            continue

        for root, dirs, files in os.walk(path):
            # Check files
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    # Check for old files
                    if get_file_age_days(filepath) >= age_threshold_days:
                        dust_bunnies["old_files"].append(filepath)

                    # Check for specific extensions (case-insensitive)
                    if extensions and any(filepath.lower().endswith(ext) for ext in extensions):
                        # Avoid duplicates if already added as an old file
                        if filepath not in dust_bunnies["extension_files"]:
                            dust_bunnies["extension_files"].append(filepath)

                except OSError as e:
                    print(f"Error accessing file {filepath}: {e}", file=sys.stderr)
                    continue

            # Check for empty directories
            if report_empty_dirs:
                for d in dirs:
                    dirpath = os.path.join(root, d)
                    try:
                        if is_empty_dir(dirpath):
                            dust_bunnies["empty_directories"].append(dirpath)
                    except OSError as e:
                        print(f"Error accessing directory {dirpath}: {e}", file=sys.stderr)
                        continue

    return dust_bunnies

def generate_report(dust_bunnies, output_file=None):
    """
    Generates a human-readable report of the found dust bunnies.
    """
    report_lines = []
    report_lines.append("--- Cosmic Dust Bunny Report ---")
    report_lines.append(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    if dust_bunnies["old_files"]:
        report_lines.append("🌌 Ancient Artifacts (Files older than threshold):")
        for item in sorted(dust_bunnies["old_files"]):
            report_lines.append(f"  - {item}")
        report_lines.append("")

    if dust_bunnies["extension_files"]:
        report_lines.append("✨ Peculiar Particles (Files with specific extensions):")
        for item in sorted(dust_bunnies["extension_files"]):
            report_lines.append(f"  - {item}")
        report_lines.append("")

    if dust_bunnies["empty_directories"]:
        report_lines.append("🕳️ Void Pockets (Empty Directories):")
        for item in sorted(dust_bunnies["empty_directories"]):
            report_lines.append(f"  - {item}")
        report_lines.append("")

    if not any(dust_bunnies.values()):
        report_lines.append("🎉 All clear! No cosmic dust bunnies detected. Your digital space is sparkling!")

    report_content = "\n".join(report_lines)

    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(report_content)
            print(f"Report saved to {output_file}")
        except IOError as e:
            print(f"Error saving report to {output_file}: {e}", file=sys.stderr)
    else:
        print(report_content)

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Bunny Collector: Identify old, temporary, or empty files/directories."
    )
    parser.add_argument(
        "--path",
        action="append",
        required=True,
        help="Directory to scan. Can be specified multiple times."
    )
    parser.add_argument(
        "--age",
        type=int,
        default=30,
        help="Report files older than this many days (default: 30)."
    )
    parser.add_argument(
        "--extensions",
        nargs="*",
        default=[],
        help="Report files with these specific extensions (e.g., .tmp .log). Case-insensitive."
    )
    parser.add_argument(
        "--report-empty-dirs",
        action="store_true",
        help="Include empty directories in the report."
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Save the report to a specified file instead of printing to console."
    )

    args = parser.parse_args()

    # Normalize extensions to start with '.' if not present and convert to lowercase for case-insensitive matching
    normalized_extensions = [ext if ext.startswith('.') else f".{ext}" for ext in args.extensions]
    normalized_extensions = [ext.lower() for ext in normalized_extensions]

    dust_bunnies = collect_dust_bunnies(
        args.path,
        args.age,
        normalized_extensions,
        args.report_empty_dirs
    )

    generate_report(dust_bunnies, args.output)

if __name__ == "__main__":
    main()
