import os
import argparse
from datetime import datetime, timedelta

def get_file_age_days(filepath):
    """Calculates the age of a file in days based on its last modification time."""
    try:
        mtime_timestamp = os.path.getmtime(filepath)
        mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
        return (datetime.now() - mtime_datetime).days
    except OSError:
        return -1 # Indicate error or non-existent file

def get_dir_age_days(dirpath):
    """Calculates the age of a directory in days based on its last modification time."""
    try:
        mtime_timestamp = os.path.getmtime(dirpath)
        mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
        return (datetime.now() - mtime_datetime).days
    except OSError:
        return -1 # Indicate error or non-existent directory

def format_size(bytes_size):
    """Formats a size in bytes to a human-readable string (KB, MB, GB)."""
    if bytes_size < 1024:
        return f"{bytes_size} Bytes"
    elif bytes_size < 1024**2:
        return f"{bytes_size / 1024:.1f} KB"
    elif bytes_size < 1024**3:
        return f"{bytes_size / (1024**2):.1f} MB"
    else:
        return f"{bytes_size / (1024**3):.1f} GB"

def find_dust_bunnies(path, max_age_days=365):
    """Scans a directory for files and directories older than max_age_days.

    Args:
        path (str): The root directory to scan.
        max_age_days (int): The maximum age in days for an item to be considered 'new'.

    Returns:
        tuple: A tuple containing (list of old files, list of old directories, total size of old files).
    """
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.")
        return [], [], 0

    old_files = []
    old_dirs = []
    total_old_file_size = 0
    current_time = datetime.now()

    for root, dirs, files in os.walk(path):
        # Check files
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mtime_timestamp = os.path.getmtime(filepath)
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
                if (current_time - mtime_datetime).days > max_age_days:
                    file_size = os.path.getsize(filepath)
                    old_files.append({
                        'path': filepath,
                        'size': file_size,
                        'mtime': mtime_datetime.strftime('%Y-%m-%d')
                    })
                    total_old_file_size += file_size
            except OSError:
                # Ignore files that might disappear during scan or permission issues
                pass
        
        # Check directories (only if they are older than max_age_days based on their own mtime)
        for d in dirs:
            dirpath = os.path.join(root, d)
            try:
                mtime_timestamp = os.path.getmtime(dirpath)
                mtime_datetime = datetime.fromtimestamp(mtime_timestamp)
                if (current_time - mtime_datetime).days > max_age_days:
                    old_dirs.append({
                        'path': dirpath,
                        'mtime': mtime_datetime.strftime('%Y-%m-%d')
                    })
            except OSError:
                pass

    return old_files, old_dirs, total_old_file_size

def main():
    parser = argparse.ArgumentParser(
        description="Finds and reports on old files and directories (digital dust bunnies).
        """
        Example:
        python3 src/collector.py --path /home/user/documents --max-age-days 365
        """
    )
    parser.add_argument('--path', type=str, required=True, help='The directory to scan.')
    parser.add_argument('--max-age-days', type=int, default=365, 
                        help='Files and directories older than this many days will be reported. Defaults to 365.')

    args = parser.parse_args()

    print(f"Scanning {args.path} for digital dust bunnies older than {args.max_age_days} days...\n")

    old_files, old_dirs, total_size = find_dust_bunnies(args.path, args.max_age_days)

    if not old_files and not old_dirs:
        print("No digital dust bunnies found! Your digital space is sparkling clean ✨.")
        return

    print("Found 🧹 Digital Dust Bunnies 🧹:\n")

    for f in old_files:
        print(f"- File: {f['path']} (Size: {format_size(f['size'])}, Last Modified: {f['mtime']})")
    for d in old_dirs:
        print(f"- Dir:  {d['path']} (Last Modified: {d['mtime']})")

    print("\n--- Summary ---")
    print(f"Total Digital Dust Bunnies Found: {len(old_files) + len(old_dirs)}")
    print(f"Total Size of Files: {format_size(total_size)}")

if __name__ == '__main__':
    main()
