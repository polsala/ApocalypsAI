import os
import json
import argparse
import time

def scan_directory(path):
    """Scans a directory and returns a dictionary of {filepath: mtime}."""
    snapshot = {}
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                # Use stat().st_mtime for more robust access to modification time
                mtime = os.stat(filepath).st_mtime
                snapshot[filepath] = mtime
            except OSError:
                # Handle cases where file might be inaccessible or disappear during scan
                # or if permissions are insufficient. Skip such files.
                pass
    return snapshot

def load_state(state_file_path):
    """Loads the previous state from a JSON file."""
    if not os.path.exists(state_file_path):
        return None
    try:
        with open(state_file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not load state from {state_file_path}: {e}. Starting fresh.")
        return None

def save_state(state_file_path, snapshot):
    """Saves the current state to a JSON file."""
    try:
        # Ensure the directory for the state file exists
        os.makedirs(os.path.dirname(state_file_path), exist_ok=True)
        with open(state_file_path, 'w') as f:
            json.dump(snapshot, f, indent=4)
    except IOError as e:
        print(f"Error: Could not save state to {state_file_path}: {e}")

def compare_snapshots(old_snapshot, new_snapshot):
    """Compares two snapshots and returns lists of new, modified, and deleted files."""
    new_files = []
    modified_files = []
    deleted_files = []

    if old_snapshot is None:
        # If no old snapshot, this is the first run. We establish a baseline
        # but don't report all files as 'new' to avoid noise.
        return [], [], []

    # Check for new and modified files
    for filepath, new_mtime in new_snapshot.items():
        if filepath not in old_snapshot:
            new_files.append(filepath)
        elif old_snapshot[filepath] != new_mtime:
            modified_files.append(filepath)

    # Check for deleted files
    for filepath in old_snapshot.keys():
        if filepath not in new_snapshot:
            deleted_files.append(filepath)

    return new_files, modified_files, deleted_files

def main():
    parser = argparse.ArgumentParser(
        description="Perform a chrono-scan of a directory to detect file system changes."
    )
    parser.add_argument(
        "--path", 
        required=True, 
        help="The directory to scan for changes."
    )
    parser.add_argument(
        "--state-file", 
        required=True, 
        help="The JSON file to store/load the last known state."
    )

    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: Directory not found at '{args.path}'")
        exit(1)

    old_snapshot = load_state(args.state_file)
    current_snapshot = scan_directory(args.path)

    new_files, modified_files, deleted_files = compare_snapshots(old_snapshot, current_snapshot)

    if old_snapshot is None:
        print(f"Chrono-scan initialized for '{args.path}'. State saved to '{args.state_file}'.")
        print(f"Found {len(current_snapshot)} files to track.")
    elif not new_files and not modified_files and not deleted_files:
        print("No significant temporal tears detected.")
    else:
        print(f"Temporal tears detected in '{args.path}':")
        if new_files:
            print("  New Files:")
            for f in new_files:
                print(f"    - {f}")
        if modified_files:
            print("  Modified Files:")
            for f in modified_files:
                print(f"    - {f}")
        if deleted_files:
            print("  Deleted Files:")
            for f in deleted_files:
                print(f"    - {f}")

    save_state(args.state_file, current_snapshot)

if __name__ == "__main__":
    main()
