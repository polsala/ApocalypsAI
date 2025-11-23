import os
import shutil
import argparse
import datetime
from typing import List, Tuple

def collect_cosmic_dust(
    directory: str,
    max_size_kb: int = 1,
    min_age_days: int = 30,
    action: str = "list",
    dustbin_dir: str = "cosmic_dustbin"
) -> List[Tuple[str, str]]:
    """
    Scans a directory for 'cosmic dust' files based on size, age, and emptiness.
    Args:
        directory (str): The root directory to scan.
        max_size_kb (int): Maximum file size in KB to be considered dust.
        min_age_days (int): Minimum age in days for a file to be considered dust.
        action (str): 'list' to just list files, 'move' to move them to a dustbin.
        dustbin_dir (str): Directory name for the dustbin if action is 'move'.
    Returns:
        List[Tuple[str, str]]: A list of (filepath, reason) for identified dust files.
    """
    dust_files = []
    now = datetime.datetime.now()
    max_size_bytes = max_size_kb * 1024

    if action == "move":
        dustbin_path = os.path.join(directory, dustbin_dir)
        os.makedirs(dustbin_path, exist_ok=True)

    for root, _, files in os.walk(directory):
        # Skip scanning the dustbin directory itself if it's within the target directory
        if action == "move" and root.startswith(os.path.abspath(dustbin_path)):
            continue

        for file in files:
            filepath = os.path.join(root, file)
            try:
                stat = os.stat(filepath)
                file_size = stat.st_size
                file_mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
                file_age_days = (now - file_mtime).days

                reasons = []
                if file_size == 0:
                    reasons.append("empty")
                if file_size < max_size_bytes:
                    reasons.append(f"small (<{max_size_kb}KB)")
                if file_age_days > min_age_days:
                    reasons.append(f"old (>{min_age_days} days)")

                if reasons:
                    reason_str = ", ".join(reasons)
                    dust_files.append((filepath, reason_str))
                    if action == "move":
                        try:
                            # Ensure unique name in dustbin if file with same name exists
                            dest_path = os.path.join(dustbin_path, os.path.basename(filepath))
                            counter = 1
                            while os.path.exists(dest_path):
                                name, ext = os.path.splitext(os.path.basename(filepath))
                                dest_path = os.path.join(dustbin_path, f"{name}_{counter}{ext}")
                                counter += 1
                            shutil.move(filepath, dest_path)
                            print(f"Moved '{{filepath}}' to '{{dest_path}}' (Reason: {{reason_str}})")
                        except Exception as e:
                            print(f"Error moving '{{filepath}}': {{e}}")
            except FileNotFoundError:
                # File might have been deleted by another process during walk
                continue
            except Exception as e:
                print(f"Error processing '{{filepath}}': {{e}}")

    return dust_files

def main():
    parser = argparse.ArgumentParser(
        description="ApocalypsAI Nightly Cosmic Dust Collector: Scans directories for small, old, or empty files."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="The root directory to scan for cosmic dust."
    )
    parser.add_argument(
        "--max-size-kb",
        type=int,
        default=1,
        help="Maximum file size in KB to consider a file 'dust'. Default: 1KB."
    )
    parser.add_argument(
        "--min-age-days",
        type=int,
        default=30,
        help="Minimum age in days for a file to be considered 'dust'. Default: 30 days."
    )
    parser.add_argument(
        "--action",
        type=str,
        choices=["list", "move"],
        default="list",
        help="Action to perform: 'list' to print identified files, 'move' to move them to a 'cosmic_dustbin' subdirectory. Default: list."
    )
    parser.add_argument(
        "--dustbin-dir",
        type=str,
        default="cosmic_dustbin",
        help="Name of the subdirectory to move files into if action is 'move'. Default: cosmic_dustbin."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{{args.directory}}' not found.")
        exit(1)

    print(f"Scanning '{{args.directory}}' for cosmic dust (max_size={{args.max_size_kb}}KB, min_age={{args.min_age_days}} days, action='{{args.action}}')...")
    dust_files = collect_cosmic_dust(
        args.directory,
        args.max_size_kb,
        args.min_age_days,
        args.action,
        args.dustbin_dir
    )

    if args.action == "list":
        if dust_files:
            print("\n--- Identified Cosmic Dust ---")
            for filepath, reason in dust_files:
                print(f"- {{filepath}} (Reason: {{reason}})")
            print(f"\nTotal dust files identified: {{len(dust_files)}}")
        else:
            print("\nNo cosmic dust found. Your digital space is pristine!")

if __name__ == "__main__":
    main()
