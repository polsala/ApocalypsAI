import os
import json
import time
import pathlib
import argparse
import logging

# --- Configuration ---
STATE_FILE_NAME = "state.json"

# --- Logging Setup ---
def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

# --- State Management ---
def load_state(state_path: pathlib.Path) -> dict:
    """Loads the state from a JSON file."""
    if state_path.exists():
        try:
            with open(state_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.warning(f"Corrupted state file detected at {state_path}. Starting fresh.")
            return {}
    return {}

def save_state(state_path: pathlib.Path, state: dict):
    """Saves the current state to a JSON file."""
    try:
        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)
        logging.info(f"State saved to {state_path}")
    except IOError as e:
        logging.error(f"Failed to save state to {state_path}: {e}")

# --- Directory Scanning ---
def scan_directory(target_dir: pathlib.Path) -> dict:
    """Scans the target directory and returns a dict of {file_path: modification_timestamp}."""
    files_info = {}
    if not target_dir.is_dir():
        logging.error(f"Target directory does not exist or is not a directory: {target_dir}")
        return files_info

    for root, _, files in os.walk(target_dir):
        for file_name in files:
            file_path = pathlib.Path(root) / file_name
            try:
                # Use os.path.getmtime for consistency with typical file system operations
                # and to avoid potential issues with Path.stat().st_mtime on some systems/mocks.
                files_info[str(file_path)] = os.path.getmtime(file_path)
            except OSError as e:
                logging.warning(f"Could not get info for {file_path}: {e}")
    return files_info

# --- Main Logic ---
def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Temporal Tear Tracker: Monitors a directory for new files."
    )
    parser.add_argument(
        "--dir",
        type=str,
        required=True,
        help="The directory to monitor for temporal tears (new files)."
    )
    args = parser.parse_args()

    target_dir = pathlib.Path(args.dir).resolve()
    logging.info(f"Monitoring directory: {target_dir}")

    # Determine the path for the state file (relative to the script's parent directory)
    script_dir = pathlib.Path(__file__).parent.parent
    state_path = script_dir / STATE_FILE_NAME

    old_state = load_state(state_path)
    current_files_info = scan_directory(target_dir)

    new_files_detected_in_run = []
    current_time = time.time()

    previous_file_paths = set(old_state.get("last_scan_files", {}).keys())

    for file_path_str, mtime in current_files_info.items():
        if file_path_str not in previous_file_paths:
            new_files_detected_in_run.append((file_path_str, mtime))

    last_tear_timestamp = old_state.get("last_tear_timestamp")

    if new_files_detected_in_run:
        logging.info("A new temporal tear has opened!")
        for file_path_str, mtime in new_files_detected_in_run:
            time_since_creation = current_time - mtime
            logging.info(f"  - New file detected: {file_path_str} (appeared {time_since_creation:.1f} seconds ago)")
        last_tear_timestamp = current_time  # Update timestamp only if new files were found
    else:
        logging.info("No new temporal tears detected. Reality remains stable.")
        if last_tear_timestamp:
            time_since_last_tear = current_time - last_tear_timestamp
            logging.info(f"It has been {time_since_last_tear:.1f} seconds since the last tear.")
        else:
            logging.info("No previous temporal tears detected. Reality is pristine.")

    new_state = {
        "last_scan_files": current_files_info,
        "last_tear_timestamp": last_tear_timestamp
    }
    save_state(state_path, new_state)
    logging.info("Current reality scan complete.")


if __name__ == "__main__":
    main()
