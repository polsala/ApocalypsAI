import os
import argparse
import sys

DEFAULT_THRESHOLD = 1024 # 1KB
QUARANTINE_DIR_NAME = '.quarantine'

def collect_dust(path_to_scan: str, threshold: int, quarantine_mode: bool) -> None:
    """
    Scans the given path for files smaller than the threshold and reports or quarantines them.
    """
    if not os.path.isdir(path_to_scan):
        print(f"Error: Path '{path_to_scan}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    found_dust = []
    for root, _, files in os.walk(path_to_scan):
        # Exclude quarantine directories from being scanned
        if QUARANTINE_DIR_NAME in root.split(os.sep):
            continue

        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    if file_size < threshold:
                        found_dust.append((file_path, file_size))
            except OSError as e:
                print(f"Warning: Could not access '{file_path}': {e}", file=sys.stderr)

    if not found_dust:
        print(f"No cosmic dust found in '{path_to_scan}' below {threshold} bytes. Your digital space is pristine!")
        return

    print(f"--- Cosmic Dust Report for '{path_to_scan}' (threshold: {threshold} bytes) ---")
    if quarantine_mode:
        print("Initiating quarantine protocol...")

    for file_path, file_size in found_dust:
        if quarantine_mode:
            parent_dir = os.path.dirname(file_path)
            quarantine_dir = os.path.join(parent_dir, QUARANTINE_DIR_NAME)
            os.makedirs(quarantine_dir, exist_ok=True)
            
            new_file_path = os.path.join(quarantine_dir, os.path.basename(file_path))
            
            # Handle potential name collisions in quarantine
            counter = 1
            original_new_file_path = new_file_path
            while os.path.exists(new_file_path):
                name, ext = os.path.splitext(os.path.basename(original_new_file_path))
                new_file_path = os.path.join(quarantine_dir, f"{name}_{counter}{ext}")
                counter += 1

            try:
                os.rename(file_path, new_file_path)
                print(f"[QUARANTINED] {file_path} ({file_size} bytes) -> {new_file_path}")
            except OSError as e:
                print(f"Error quarantining '{file_path}': {e}", file=sys.stderr)
        else:
            print(f"[DUST] {file_path} ({file_size} bytes)")

    if quarantine_mode:
        print("Quarantine protocol complete. Review the .quarantine directories for further action.")
    print("------------------------------------------------------------------")


def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Scans directories for small, forgotten files."
    )
    parser.add_argument(
        "path_to_scan",
        type=str,
        help="The root directory to begin the cosmic dust sweep."
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=DEFAULT_THRESHOLD,
        help=f"Maximum file size (in bytes) to consider as 'cosmic dust'. Default: {DEFAULT_THRESHOLD} bytes."
    )
    parser.add_argument(
        "--quarantine",
        action="store_true",
        help="If provided, identified 'dust' files will be moved to a .quarantine subdirectory."
    )

    args = parser.parse_args()

    collect_dust(args.path_to_scan, args.threshold, args.quarantine)


if __name__ == "__main__":
    main()
