import argparse
import os
import shutil
import sys
from pathlib import Path

def collect_cosmic_dust(
    root_path: Path,
    threshold: int,
    action: str,
    archive_dir: Path | None,
    dry_run: bool,
) -> list[str]:
    """
    Scans a directory for files smaller than a threshold and performs an action.

    Args:
        root_path: The root directory to scan.
        threshold: Maximum file size in bytes to consider as 'dust'.
        action: 'list', 'archive', or 'delete'.
        archive_dir: Directory for archiving files (required if action is 'archive').
        dry_run: If True, only report actions, don't perform them.

    Returns:
        A list of messages describing the actions taken or proposed.
    """
    messages = []
    if not root_path.is_dir():
        messages.append(f"Error: Path '{root_path}' is not a valid directory.")
        return messages

    if action == 'archive' and not archive_dir:
        messages.append("Error: --archive-dir is required when action is 'archive'.")
        return messages

    if action == 'archive' and archive_dir and not dry_run:
        archive_dir.mkdir(parents=True, exist_ok=True)

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            file_path = Path(dirpath) / filename
            try:
                file_size = file_path.stat().st_size
                if file_size <= threshold:
                    if action == 'list':
                        messages.append(f"Found dust: {file_path} ({file_size} bytes)")
                    elif action == 'archive':
                        if archive_dir:
                            dest_path = archive_dir / file_path.name
                            if not dry_run:
                                shutil.move(file_path, dest_path)
                                messages.append(f"Archived: {file_path} -> {dest_path}")
                            else:
                                messages.append(f"Dry run: Would archive {file_path} -> {dest_path}")
                        else:
                            messages.append(f"Error: Archive directory not specified for {file_path}")
                    elif action == 'delete':
                        if not dry_run:
                            file_path.unlink()
                            messages.append(f"Deleted: {file_path}")
                        else:
                            messages.append(f"Dry run: Would delete {file_path}")
            except OSError as e:
                messages.append(f"Warning: Could not process {file_path}: {e}")

    if not messages:
        messages.append(f"No cosmic dust found in '{root_path}' below {threshold} bytes.")

    return messages

def main():
    parser = argparse.ArgumentParser(
        description="Collects cosmic dust (small files) from specified directories."
    )
    parser.add_argument(
        "--path",
        type=Path,
        required=True,
        help="The root directory to scan for cosmic dust.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=1024,
        help="Maximum file size in bytes to consider as 'cosmic dust'. Default: 1024 bytes (1KB).",
    )
    parser.add_argument(
        "--action",
        choices=['list', 'archive', 'delete'],
        default='list',
        help="Action to perform on identified files. Default: 'list'.",
    )
    parser.add_argument(
        "--archive-dir",
        type=Path,
        help="The directory where files will be moved when action is 'archive'. Required for 'archive' action.",
    )
    parser.add_argument(
        "--dry-run",
        action='store_true',
        help="If set, no files will be moved or deleted. Only reports what would happen.",
    )

    args = parser.parse_args()

    if args.action == 'archive' and not args.archive_dir:
        print("Error: --archive-dir is required when action is 'archive'.", file=sys.stderr)
        sys.exit(1)

    results = collect_cosmic_dust(
        args.path,
        args.threshold,
        args.action,
        args.archive_dir,
        args.dry_run,
    )

    for msg in results:
        print(msg)

    if any("Error:" in msg for msg in results):
        sys.exit(1)
    elif any("Warning:" in msg for msg in results):
        sys.exit(0) # Warnings are not critical failures
    elif "No cosmic dust found" in results[0] and len(results) == 1:
        sys.exit(2) # No-op, nothing to change
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
