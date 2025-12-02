import os
import argparse
import sys

def collect_dust(root_dir: str, threshold_bytes: int, action: str, quarantine_dir: str = None) -> list:
    """
    Scans a directory for files smaller than a given threshold and performs an action.

    Args:
        root_dir (str): The root directory to scan.
        threshold_bytes (int): Maximum file size in bytes to be considered cosmic dust.
        action (str): 'list' to print files, 'quarantine' to move them.
        quarantine_dir (str, optional): Directory to move files into if action is 'quarantine'.
                                        Required if action is 'quarantine'.

    Returns:
        list: A list of paths to the files identified as cosmic dust.
    """
    if not os.path.isdir(root_dir):
        print(f"Error: Root directory '{root_dir}' does not exist or is not a directory.", file=sys.stderr)
        return []

    if action == 'quarantine' and not quarantine_dir:
        print("Error: --quarantine-dir is required when action is 'quarantine'.", file=sys.stderr)
        return []

    dust_files = []
    print(f"Scanning '{root_dir}' for cosmic dust (files <= {threshold_bytes} bytes)...")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            try:
                file_size = os.path.getsize(file_path)
                if file_size <= threshold_bytes:
                    dust_files.append(file_path)
            except OSError as e:
                print(f"Warning: Could not access '{file_path}': {e}", file=sys.stderr)

    if not dust_files:
        print("No cosmic dust found. Your space is sparkling clean! ✨")
        return []

    print(f"Found {len(dust_files)} pieces of cosmic dust.")

    if action == 'list':
        print("--- Cosmic Dust List ---")
        for f in dust_files:
            print(f"- {f} ({os.path.getsize(f)} bytes)")
        print("------------------------")
    elif action == 'quarantine':
        print(f"Moving cosmic dust to quarantine at '{quarantine_dir}'...")
        if not os.path.exists(quarantine_dir):
            try:
                os.makedirs(quarantine_dir)
                print(f"Created quarantine directory: '{quarantine_dir}'")
            except OSError as e:
                print(f"Error: Could not create quarantine directory '{quarantine_dir}': {e}", file=sys.stderr)
                return []

        for file_path in dust_files:
            try:
                # Preserve relative path structure within quarantine_dir
                relative_path = os.path.relpath(file_path, root_dir)
                dest_path = os.path.join(quarantine_dir, relative_path)
                dest_dir = os.path.dirname(dest_path)

                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                os.rename(file_path, dest_path)
                print(f"Quarantined: '{file_path}' -> '{dest_path}'")
            except OSError as e:
                print(f"Error quarantining '{file_path}': {e}", file=sys.stderr)
    return dust_files

def main():
    parser = argparse.ArgumentParser(description="Collects cosmic dust (small/empty files) from a directory.")
    parser.add_argument('--path', type=str, required=True, help="The root directory to scan for cosmic dust.")
    parser.add_argument('--threshold', type=int, default=1024, 
                        help="Maximum file size in bytes to be considered cosmic dust (default: 1024 bytes).")
    parser.add_argument('--action', type=str, choices=['list', 'quarantine'], default='list',
                        help="Action to perform: 'list' files or 'quarantine' them (default: list).")
    parser.add_argument('--quarantine-dir', type=str, 
                        help="Directory to move cosmic dust files into when action is 'quarantine'. Required for 'quarantine' action.")

    args = parser.parse_args()

    if args.action == 'quarantine' and not args.quarantine_dir:
        parser.error("argument --quarantine-dir is required when --action is 'quarantine'")

    collect_dust(args.path, args.threshold, args.action, args.quarantine_dir)

if __name__ == '__main__':
    main()
