import os
import sys
import time
from datetime import datetime, timedelta

def find_dust_bunnies(path, age_threshold_days=90):
    """
    Scans a directory for 'digital dust bunnies':
    - Empty files
    - Empty directories
    - Files with common temporary/backup extensions (.tmp, .bak, ~)
    - Files older than age_threshold_days (excluding temp/backup files)

    Args:
        path (str): The root directory to scan.
        age_threshold_days (int): Files older than this many days are considered old.

    Returns:
        dict: A dictionary containing lists of identified dust bunnies.
    """
    dust_bunnies = {
        "empty_files": [],
        "empty_dirs": [],
        "temp_files": [],
        "old_files": []
    }
    current_time = time.time()
    age_threshold_timestamp = current_time - (age_threshold_days * 24 * 60 * 60)

    temp_extensions = ('.tmp', '.bak', '~', '.log', '.old', '.swp') # Common temporary/backup extensions

    for root, dirs, files in os.walk(path):
        # Check for empty files, temp files, and old files
        for file_name in files:
            full_path = os.path.join(root, file_name)
            if os.path.isfile(full_path): # Ensure it's a file (os.walk might list broken symlinks as files)
                if os.path.getsize(full_path) == 0:
                    dust_bunnies["empty_files"].append(full_path)
                elif file_name.lower().endswith(temp_extensions):
                    dust_bunnies["temp_files"].append(full_path)
                else:
                    # Check for old files, but only if not already classified as temp
                    try:
                        mtime = os.path.getmtime(full_path)
                        if mtime < age_threshold_timestamp:
                            dust_bunnies["old_files"].append(full_path)
                    except OSError:
                        # Mock rationale: Handle cases where file might be deleted between os.walk and getmtime.
                        pass

        # Check for empty directories (if current root has no files and no subdirs)
        if not files and not dirs:
            dust_bunnies["empty_dirs"].append(root)

    return dust_bunnies

def generate_report(dust_bunnies, path):
    """
    Generates a whimsical report from the identified dust bunnies.
    """
    report_lines = [
        f"--- Digital Dust Bunny Sweeper Report for '{path}' ---",
        "",
        "Greetings, brave maintainer! Your digital realm has been scanned for lurking dust bunnies.",
        "Fear not, for we have uncovered their hiding spots!",
        ""
    ]

    total_bunnies = sum(len(v) for v in dust_bunnies.values())

    if total_bunnies == 0:
        report_lines.append("✨ Huzzah! Your digital space is sparkling clean! No dust bunnies found. ✨")
    else:
        if dust_bunnies["empty_files"]:
            report_lines.append(f"🕳️ Empty Files ({len(dust_bunnies['empty_files'])}): These files are just taking up space, dreaming of content.")
            for bunny in dust_bunnies["empty_files"]:
                report_lines.append(f"  - {bunny}")
            report_lines.append("")

        if dust_bunnies["empty_dirs"]:
            report_lines.append(f"🚪 Empty Directories ({len(dust_bunnies['empty_dirs'])}): Echoing chambers of forgotten data.")
            for bunny in dust_bunnies["empty_dirs"]:
                report_lines.append(f"  - {bunny}")
            report_lines.append("")

        if dust_bunnies["temp_files"]:
            report_lines.append(f"⏳ Temporary & Backup Files ({len(dust_bunnies['temp_files'])}): These were just visiting, now they're overstaying their welcome.")
            for bunny in dust_bunnies["temp_files"]:
                report_lines.append(f"  - {bunny}")
            report_lines.append("")

        if dust_bunnies["old_files"]:
            report_lines.append(f"👴 Ancient Files ({len(dust_bunnies['old_files'])}): Relics from a bygone era, perhaps it's time to archive them?")
            for bunny in dust_bunnies["old_files"]:
                report_lines.append(f"  - {bunny}")
            report_lines.append("")

        report_lines.append(f"🧹 Total Digital Dust Bunnies Found: {total_bunnies}")
        report_lines.append("Consider giving them a good sweep!")

    report_lines.append("\n--- End of Report ---")
    return "\n".join(report_lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python sweeper.py <path_to_scan> [age_threshold_days]")
        sys.exit(1)

    scan_path = sys.argv[1]
    age_threshold_days = 90 # Default
    if len(sys.argv) > 2:
        try:
            age_threshold_days = int(sys.argv[2])
            if age_threshold_days < 0:
                raise ValueError
        except ValueError:
            print("Error: age_threshold_days must be a non-negative integer.")
            sys.exit(1)

    if not os.path.isdir(scan_path):
        print(f"Error: Path '{scan_path}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning '{scan_path}' for digital dust bunnies (age threshold: {age_threshold_days} days)...")
    bunnies = find_dust_bunnies(scan_path, age_threshold_days)
    report = generate_report(bunnies, scan_path)
    print(report)

if __name__ == "__main__":
    main()
