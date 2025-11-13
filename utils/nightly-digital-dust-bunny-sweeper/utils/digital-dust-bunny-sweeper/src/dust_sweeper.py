import os
import sys
import time
from datetime import datetime, timedelta

def find_dust_bunnies(root_dir, age_threshold_days=30):
    """
    Scans the given root directory for 'digital dust bunnies'.
    Reports:
    - Empty directories
    - Zero-byte files
    - Old log files (.log, not modified in age_threshold_days)
    - Common system junk files (.DS_Store, Thumbs.db, desktop.ini)
    """
    dust_bunnies = []
    now = datetime.now()

    if not os.path.isdir(root_dir):
        print(f"Error: Directory not found or not a directory: {root_dir}", file=sys.stderr)
        return []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check for empty directories
        if not dirnames and not filenames:
            dust_bunnies.append(f"[EMPTY DIRECTORY] {dirpath}")

        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            # Handle cases where file might be inaccessible or disappear during walk
            try:
                # Check for zero-byte files
                if os.path.getsize(filepath) == 0:
                    dust_bunnies.append(f"[ZERO-BYTE FILE] {filepath} (0 bytes)")

                # Check for old log files
                if filename.lower().endswith(".log"):
                    mtime_timestamp = os.path.getmtime(filepath)
                    mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
                    if (now - mtime_datetime) > timedelta(days=age_threshold_days):
                        dust_bunnies.append(f"[OLD LOG FILE] {filepath} (Last modified: {mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')})")

            except OSError:
                continue # Skip inaccessible files

            # Check for system junk files
            if filename.lower() in [".ds_store", "thumbs.db", "desktop.ini"]:
                dust_bunnies.append(f"[SYSTEM JUNK] {filepath}")

    return dust_bunnies

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/dust_sweeper.py <directory_to_scan>", file=sys.stderr)
        sys.exit(1)

    scan_dir = sys.argv[1]
    print(f"Scanning {scan_dir}...\n")

    bunnies = find_dust_bunnies(scan_dir)

    print(f"🧹 Digital Dust Bunny Report for {scan_dir} 🧹\n")
    if bunnies:
        for bunny in bunnies:
            print(bunny)
        print(f"\nFound {len(bunnies)} digital dust bunnies. Time to tidy up!")
    else:
        print("No digital dust bunnies found. Your digital space is sparkling clean!")

if __name__ == "__main__":
    main()
