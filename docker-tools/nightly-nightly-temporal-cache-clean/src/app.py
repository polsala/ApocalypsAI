import os
import sys
import time
from datetime import datetime, timedelta
import argparse

def get_env_var(name, default=None, type_func=str):
    """
    Retrieves an environment variable, applies a type conversion, and handles errors.
    """
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return type_func(value)
    except ValueError:
        print(f"Warning: Environment variable {name} has invalid format ('{value}'). Using default: {default}", file=sys.stderr)
        return default

def clean_temporal_cache(target_dirs_str, age_days, dry_run):
    """
    Sweeps away files older than age_days in specified directories.
    """
    target_dirs = [d.strip() for d in target_dirs_str.split(',') if d.strip()]
    if not target_dirs:
        print("No target directories specified. Nothing to sweep!", file=sys.stderr)
        return

    print(f"Initiating Temporal Cache Sweep for: {', '.join(target_dirs)}")
    print(f"Targeting files older than {age_days} days.")
    print(f"Mode: {'DRY RUN (no files will be deleted)' if dry_run else 'LIVE SWEEP (files will be deleted)'}")
    print("-" * 50)

    cutoff_time = datetime.now() - timedelta(days=age_days)
    swept_count = 0
    swept_size = 0

    for target_dir in target_dirs:
        if not os.path.isdir(target_dir):
            print(f"Warning: Target directory '{target_dir}' does not exist or is not a directory. Skipping.", file=sys.stderr)
            continue

        print(f"\nScanning '{target_dir}' for temporal detritus...")
        for root, _, files in os.walk(target_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    # Check if it's actually a file (not a broken symlink, etc.)
                    if not os.path.isfile(file_path):
                        continue

                    mtime_timestamp = os.path.getmtime(file_path)
                    mtime_datetime = datetime.fromtimestamp(mtime_timestamp)

                    if mtime_datetime < cutoff_time:
                        file_size = os.path.getsize(file_path)
                        print(f"  Found ancient artifact: {file_path} (Modified: {mtime_datetime.strftime('%Y-%m-%d %H:%M:%S')}, Size: {file_size} bytes)")
                        if not dry_run:
                            os.remove(file_path)
                            print(f"    *Poof!* {file_name} vanished into the temporal void.")
                            swept_count += 1
                            swept_size += file_size
                        else:
                            print(f"    (Dry run: Would have swept {file_name})")
                except OSError as e:
                    print(f"  Error processing {file_path}: {e}", file=sys.stderr)
                except Exception as e:
                    print(f"  Unexpected error with {file_path}: {e}", file=sys.stderr)

    print("\n" + "-" * 50)
    if dry_run:
        print(f"Temporal Cache Sweep (DRY RUN) complete. Identified {swept_count} artifacts totaling {swept_size} bytes for sweeping.")
    else:
        print(f"Temporal Cache Sweep (LIVE) complete. Swept away {swept_count} artifacts totaling {swept_size} bytes.")
    print("The digital realm feels a bit lighter now!")

if __name__ == "__main__":
    # Default values from environment variables
    target_dirs_env = get_env_var("TARGET_DIRS", "/tmp/cache", str)
    age_days_env = get_env_var("AGE_DAYS", 30, int)
    dry_run_env = get_env_var("DRY_RUN", True, lambda x: x.lower() == 'true')

    parser = argparse.ArgumentParser(description="Temporal Cache Cleaner: Sweep away old files.")
    parser.add_argument('--dirs', type=str, default=target_dirs_env,
                        help='Comma-separated list of directories to scan. Overrides TARGET_DIRS env var.')
    parser.add_argument('--age', type=int, default=age_days_env,
                        help='Files older than this many days will be swept. Overrides AGE_DAYS env var.')
    parser.add_argument('--live', action='store_false', dest='dry_run', default=dry_run_env,
                        help='Perform live deletion. By default, it\'s a dry run. Overrides DRY_RUN env var.')
    args = parser.parse_args()

    clean_temporal_cache(args.dirs, args.age, args.dry_run)
