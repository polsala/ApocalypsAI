import os
import shutil
import argparse
from datetime import datetime, timedelta

def find_dust_bunnies(scan_path, age_days, max_size_kb, verbose=False):
    """
    Scans a directory for files that are older than `age_days` and smaller than `max_size_kb`.
    Returns a list of paths to these 'dust bunny' files.
    """
    dust_bunnies = []
    now = datetime.now()
    age_threshold = now - timedelta(days=age_days)
    max_size_bytes = max_size_kb * 1024

    if verbose:
        print(f"Scanning '{scan_path}' for files older than {age_days} days and <= {max_size_kb} KB...")

    for root, _, files in os.walk(scan_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                stat = os.stat(file_path)
                last_modified_timestamp = stat.st_mtime
                file_size = stat.st_size
                last_modified_dt = datetime.fromtimestamp(last_modified_timestamp)

                is_old = last_modified_dt < age_threshold
                is_small = file_size <= max_size_bytes

                if is_old and is_small:
                    dust_bunnies.append({
                        'path': file_path,
                        'size': file_size,
                        'last_modified': last_modified_dt
                    })
                    if verbose:
                        print(f"  Found dust bunny: {file_path} (Size: {file_size/1024:.2f} KB, Modified: {last_modified_dt.strftime('%Y-%m-%d')})")
            except OSError as e:
                if verbose:
                    print(f"  Warning: Could not access {file_path}: {e}")
                continue
    return dust_bunnies

def quarantine_dust_bunnies(dust_bunnies, quarantine_dir, verbose=False):
    """
    Moves identified dust bunnies to a specified quarantine directory.
    """
    if not dust_bunnies:
        print("No dust bunnies to quarantine.")
        return

    os.makedirs(quarantine_dir, exist_ok=True)
    print(f"Moving {len(dust_bunnies)} dust bunnies to quarantine zone: '{quarantine_dir}'")

    for bunny in dust_bunnies:
        src_path = bunny['path']
        dest_path = os.path.join(quarantine_dir, os.path.basename(src_path))
        try:
            shutil.move(src_path, dest_path)
            if verbose:
                print(f"  Quarantined: '{src_path}' -> '{dest_path}'")
        except Exception as e:
            print(f"  Error quarantining '{src_path}': {e}")

def delete_dust_bunnies(dust_bunnies, verbose=False):
    """
    Permanently deletes identified dust bunnies.
    """
    if not dust_bunnies:
        print("No dust bunnies to delete.")
        return

    print(f"Permanently deleting {len(dust_bunnies)} dust bunnies. This action is irreversible!")
    confirm = input("Type 'DELETE' to confirm: ")
    if confirm != 'DELETE':
        print("Deletion cancelled.")
        return

    for bunny in dust_bunnies:
        file_path = bunny['path']
        try:
            os.remove(file_path)
            if verbose:
                print(f"  Deleted: '{file_path}'")
        except Exception as e:
            print(f"  Error deleting '{file_path}': {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Dust Bunny Collector: Identify and manage old, small files."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        default='.', 
        help='The directory to scan for dust bunnies. Defaults to current directory.'
    )
    parser.add_argument(
        '--age-days', 
        type=int, 
        default=90, 
        help='Files older than this many days (last modified) are considered dust bunnies. Default: 90.'
    )
    parser.add_argument(
        '--max-size-kb', 
        type=int, 
        default=1, 
        help='Files smaller than or equal to this size in KB are considered dust bunnies. Default: 1 (1KB).'
    )
    parser.add_argument(
        '--quarantine', 
        type=str, 
        help='Move identified dust bunnies to this directory. Creates if not exists.'
    )
    parser.add_argument(
        '--delete', 
        action='store_true', 
        help='Permanently delete identified dust bunnies. USE WITH EXTREME CAUTION!'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Print more detailed output during scanning.'
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Scan path '{args.path}' is not a valid directory.")
        exit(1)

    dust_bunnies = find_dust_bunnies(
        args.path, args.age_days, args.max_size_kb, args.verbose
    )

    if not dust_bunnies:
        print("No Cosmic Dust Bunnies found in the specified parameters. Your digital space is pristine!")
        return

    print(f"\nFound {len(dust_bunnies)} Cosmic Dust Bunnies:")
    for bunny in dust_bunnies:
        print(f"  - {bunny['path']} (Size: {bunny['size']/1024:.2f} KB, Modified: {bunny['last_modified'].strftime('%Y-%m-%d %H:%M:%S')})")

    if args.quarantine:
        quarantine_dust_bunnies(dust_bunnies, args.quarantine, args.verbose)
    elif args.delete:
        delete_dust_bunnies(dust_bunnies, args.verbose)
    else:
        print("\nTo take action, use --quarantine <directory> or --delete.")

if __name__ == '__main__':
    main()
