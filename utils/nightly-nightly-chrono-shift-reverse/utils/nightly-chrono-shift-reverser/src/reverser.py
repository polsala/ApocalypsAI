import os
import shutil
import datetime
import time
import argparse

QUARANTINE_DIR_NAME = ".quarantine"

def _get_quarantine_path(target_dir):
    return os.path.join(target_dir, QUARANTINE_DIR_NAME)

def _get_timestamp_dir_name():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def clean_old_files(target_dir: str, age_days: int):
    """
    Moves files older than `age_days` from `target_dir` to a timestamped quarantine directory.
    """
    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.")
        return

    quarantine_base = _get_quarantine_path(target_dir)
    current_quarantine_batch_dir = os.path.join(quarantine_base, _get_timestamp_dir_name())

    os.makedirs(current_quarantine_batch_dir, exist_ok=True)
    print(f"Created quarantine batch directory: {current_quarantine_batch_dir}")

    cutoff_time = time.time() - (age_days * 24 * 60 * 60)
    moved_count = 0

    for root, _, files in os.walk(target_dir):
        # Skip the quarantine directory itself
        if root.startswith(quarantine_base):
            continue

        for file_name in files:
            file_path = os.path.join(root, file_name)
            if os.path.isfile(file_path):
                try:
                    mod_time = os.path.getmtime(file_path)
                    if mod_time < cutoff_time:
                        relative_path = os.path.relpath(file_path, target_dir)
                        destination_path = os.path.join(current_quarantine_batch_dir, relative_path)
                        
                        # Ensure the destination subdirectory exists
                        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                        
                        shutil.move(file_path, destination_path)
                        print(f"Moved '{file_path}' to '{destination_path}'")
                        moved_count += 1
                except OSError as e:
                    print(f"Warning: Could not process '{file_path}': {e}")
    
    if moved_count == 0:
        print("No old files found to quarantine. Removing empty batch directory.")
        # Clean up the empty batch directory if nothing was moved
        try:
            os.rmdir(current_quarantine_batch_dir)
            # Also remove the base quarantine dir if it becomes empty
            if not os.listdir(quarantine_base):
                os.rmdir(quarantine_base)
        except OSError as e:
            print(f"Warning: Could not remove empty quarantine directory '{current_quarantine_batch_dir}': {e}")
    else:
        print(f"Successfully quarantined {moved_count} files.")

def list_quarantined_batches(target_dir: str):
    """
    Lists all timestamped quarantine batches within the target directory.
    """
    quarantine_base = _get_quarantine_path(target_dir)
    if not os.path.isdir(quarantine_base):
        print(f"No quarantine directory found at '{quarantine_base}'.")
        return

    batches = [d for d in os.listdir(quarantine_base) if os.path.isdir(os.path.join(quarantine_base, d))]
    if not batches:
        print(f"No quarantined batches found in '{quarantine_base}'.")
        return

    print(f"Quarantined batches in '{target_dir}':")
    for batch in sorted(batches):
        print(f"- {batch}")

def restore_batch(target_dir: str, batch_name: str):
    """
    Restores all files from a specific quarantined batch back to the target directory.
    """
    quarantine_base = _get_quarantine_path(target_dir)
    batch_path = os.path.join(quarantine_base, batch_name)

    if not os.path.isdir(batch_path):
        print(f"Error: Quarantine batch '{batch_name}' not found at '{batch_path}'.")
        return

    restored_count = 0
    for root, _, files in os.walk(batch_path):
        for file_name in files:
            source_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(source_path, batch_path)
            destination_path = os.path.join(target_dir, relative_path)
            
            # Ensure the destination subdirectory exists
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            try:
                shutil.move(source_path, destination_path)
                print(f"Restored '{source_path}' to '{destination_path}'")
                restored_count += 1
            except OSError as e:
                print(f"Warning: Could not restore '{source_path}': {e}")
    
    # Clean up the empty batch directory after restoration
    try:
        shutil.rmtree(batch_path)
        print(f"Removed empty quarantine batch directory: {batch_path}")
        # Also remove the base quarantine dir if it becomes empty
        if not os.listdir(quarantine_base):
            os.rmdir(quarantine_base)
    except OSError as e:
        print(f"Warning: Could not remove empty quarantine directory '{batch_path}': {e}")

    print(f"Successfully restored {restored_count} files from batch '{batch_name}'.")

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Chrono-Shift Reverser: Safely quarantine and restore old files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Clean command
    clean_parser = subparsers.add_parser("clean", help="Clean old files by moving them to quarantine.")
    clean_parser.add_argument("target_dir", help="The directory to clean.")
    clean_parser.add_argument("--age", type=int, default=7, help="Files older than this many days will be quarantined. Default is 7.")

    # List command
    list_parser = subparsers.add_parser("list", help="List quarantined batches.")
    list_parser.add_argument("target_dir", help="The directory where quarantine batches are located.")

    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore a specific quarantined batch.")
    restore_parser.add_argument("target_dir", help="The directory where quarantine batches are located.")
    restore_parser.add_argument("--batch", required=True, help="The name of the batch to restore (e.g., 2023-10-27_14-30-00).")

    args = parser.parse_args()

    if args.command == "clean":
        clean_old_files(args.target_dir, args.age)
    elif args.command == "list":
        list_quarantined_batches(args.target_dir)
    elif args.command == "restore":
        restore_batch(args.target_dir, args.batch)

if __name__ == "__main__":
    main()
