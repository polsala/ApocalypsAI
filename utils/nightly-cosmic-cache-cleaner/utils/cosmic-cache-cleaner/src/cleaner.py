import os
import sys
import platform
import datetime
import argparse
import shutil

def get_cache_paths():
    """Returns a list of common cache directories based on the operating system."""
    paths = []
    system = platform.system()

    if system == 'Windows':
        local_app_data = os.environ.get('LOCALAPPDATA')
        temp_dir = os.environ.get('TEMP')
        if local_app_data: paths.append(os.path.join(local_app_data, 'Temp'))
        if temp_dir: paths.append(temp_dir)
        # Common application caches
        if local_app_data: paths.append(os.path.join(local_app_data, 'pip', 'cache'))
        if local_app_data: paths.append(os.path.join(local_app_data, 'npm-cache'))
    elif system == 'Darwin':  # macOS
        home = os.path.expanduser('~')
        paths.append(os.path.join(home, 'Library', 'Caches'))
        paths.append('/Library/Caches') # System-wide caches
        # Common application caches
        paths.append(os.path.join(home, 'Library', 'Caches', 'pip'))
        paths.append(os.path.join(home, 'Library', 'Caches', 'npm'))
    else:  # Linux and other Unix-like systems
        xdg_cache_home = os.environ.get('XDG_CACHE_HOME', os.path.join(os.path.expanduser('~'), '.cache'))
        paths.append(xdg_cache_home)
        paths.append('/var/cache')
        # Common application caches
        paths.append(os.path.join(xdg_cache_home, 'pip'))
        paths.append(os.path.join(xdg_cache_home, 'npm'))

    # Filter out paths that don't exist or are not directories
    return [p for p in paths if os.path.isdir(p)]

def scan_directory(path, min_age_days, min_size_mb):
    """Scans a directory for files older than min_age_days or larger than min_size_mb."""
    files_to_clean = []
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=min_age_days)
    min_size_bytes = min_size_mb * 1024 * 1024

    for root, _, files in os.walk(path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # Skip broken symlinks or inaccessible files
                if not os.path.exists(file_path):
                    continue

                file_stat = os.stat(file_path)
                file_mtime = datetime.datetime.fromtimestamp(file_stat.st_mtime)
                file_size = file_stat.st_size

                if file_mtime < cutoff_date or file_size > min_size_bytes:
                    files_to_clean.append({
                        'path': file_path,
                        'size': file_size,
                        'mtime': file_mtime
                    })
            except OSError as e:
                print(f"🌌 Warning: Could not access {file_path} - {e}", file=sys.stderr)
                continue
    return files_to_clean

def format_size(size_bytes):
    """Formats bytes into a human-readable string (MB, GB)."""
    if size_bytes < 1024 * 1024: # Less than 1 MB
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024: # Less than 1 GB
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def generate_report(files_to_clean):
    """Generates a formatted report of files to be cleaned."""
    if not files_to_clean:
        print("\n✨ Cosmic Debris Report ✨\n")
        print("No significant cosmic dust detected. Your system is sparkling clean! ✨")
        return 0

    total_size = sum(f['size'] for f in files_to_clean)

    print("\n✨ Cosmic Debris Report ✨\n")
    print(f"Identified {len(files_to_clean)} pieces of space junk:\n")

    for f in files_to_clean:
        print(f"- {f['path']} ({format_size(f['size'])}, last modified: {f['mtime'].strftime('%Y-%m-%d')})")

    print(f"\nTotal estimated mass of cosmic dust to be purged: {format_size(total_size)}")
    return total_size

def delete_files(files_to_clean, force=False):
    """Deletes the specified files."""
    if not files_to_clean:
        print("No files to delete. Mission accomplished (or no debris found)!\n")
        return

    if not force:
        confirmation = input("\nAre you sure you want to initiate orbital decay protocol (delete these files)? (yes/no): ")
        if confirmation.lower() != 'yes':
            print("Deletion aborted. Cosmic dust remains for now.\n")
            return

    print("\nInitiating orbital decay protocol...\n")
    deleted_count = 0
    deleted_size = 0
    for f in files_to_clean:
        try:
            if os.path.isfile(f['path']):
                os.remove(f['path'])
                print(f"🚀 Purged: {f['path']}")
                deleted_count += 1
                deleted_size += f['size']
            elif os.path.isdir(f['path']): # Handle empty directories that might be left after file deletion
                shutil.rmtree(f['path'])
                print(f"🚀 Purged directory: {f['path']}")
                deleted_count += 1
                deleted_size += f['size'] # This might not be accurate for directories, but good enough for a utility
        except OSError as e:
            print(f"🌌 Error purging {f['path']}: {e}", file=sys.stderr)

    print(f"\nOrbital decay protocol complete. {deleted_count} items purged, {format_size(deleted_size)} reclaimed.\n")

def main():
    parser = argparse.ArgumentParser(
        description="Cosmic Cache Cleaner: Purge digital cosmic dust from your system."
    )
    parser.add_argument('--dry-run', action='store_true', default=True,
                        help='Scan and report, but do not delete any files (default).')
    parser.add_argument('--delete', action='store_true',
                        help='Enable deletion of identified files. Will prompt for confirmation unless --force is used.')
    parser.add_argument('--force', action='store_true',
                        help='Use with --delete to skip the confirmation prompt. Use with extreme caution!')
    parser.add_argument('--age', type=int, default=30,
                        help='Only consider files older than this many days (default: 30).')
    parser.add_argument('--size', type=int, default=100,
                        help='Only consider files larger than this many megabytes (default: 100).')
    parser.add_argument('--paths', nargs='*', default=[],
                        help='Specify custom directories to scan instead of default system caches.')

    args = parser.parse_args()

    if args.delete:
        args.dry_run = False # If delete is specified, dry-run is implicitly false

    print("🌌 Initiating Cosmic Cache Scan... 🌌\n")

    target_paths = args.paths if args.paths else get_cache_paths()

    if not target_paths:
        print("🌌 No cache paths found or specified. Exiting.\n")
        sys.exit(0)

    all_files_to_clean = []
    for path in target_paths:
        if os.path.isdir(path):
            print(f"🚀 Analyzing: {path}")
            all_files_to_clean.extend(scan_directory(path, args.age, args.size))
        else:
            print(f"🌌 Warning: Path not found or not a directory: {path}", file=sys.stderr)

    total_size_reported = generate_report(all_files_to_clean)

    if not args.dry_run and args.delete:
        if total_size_reported > 0:
            delete_files(all_files_to_clean, args.force)
        else:
            print("No cosmic dust to purge. Your system is already pristine!\n")
    elif args.dry_run:
        print("\nTo proceed with orbital decay protocol (deletion), run with --delete.\n")

if __name__ == '__main__':
    main()
