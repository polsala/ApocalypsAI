import hashlib
import json
from pathlib import Path
from typing import Dict, Any

def _calculate_file_hash(filepath: Path) -> str:
    """Calculates the SHA256 hash of a file's content."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def take_snapshot(target_path: Path) -> Dict[str, str]:
    """
    Takes a snapshot of files in a given path (file or directory).
    Returns a dictionary mapping relative file paths to their SHA256 hashes.
    """
    snapshot = {}
    if not target_path.exists():
        raise FileNotFoundError(f"Path does not exist: {target_path}")

    if target_path.is_file():
        snapshot[target_path.name] = _calculate_file_hash(target_path)
    elif target_path.is_dir():
        for item in target_path.rglob('*'): # rglob for recursive glob
            if item.is_file():
                relative_path = item.relative_to(target_path).as_posix()
                snapshot[relative_path] = _calculate_file_hash(item)
    return snapshot

def compare_snapshots(
    snapshot1: Dict[str, str],
    snapshot2: Dict[str, str]
) -> Dict[str, Any]:
    """
    Compares two snapshots and returns a dictionary of changes.
    snapshot1 is considered the 'old' state, snapshot2 the 'new' state.
    """
    changes = {
        "new_files": [],
        "deleted_files": [],
        "modified_files": [],
        "unchanged_files": []
    }

    files1 = set(snapshot1.keys())
    files2 = set(snapshot2.keys())

    # Deleted files
    for f in files1 - files2:
        changes["deleted_files"].append(f)

    # New files
    for f in files2 - files1:
        changes["new_files"].append(f)

    # Modified or Unchanged files
    for f in files1.intersection(files2):
        if snapshot1[f] != snapshot2[f]:
            changes["modified_files"].append(f)
        else:
            changes["unchanged_files"].append(f)

    return changes

def save_snapshot(snapshot: Dict[str, str], filepath: Path):
    """Saves a snapshot to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(snapshot, f, indent=2)

def load_snapshot(filepath: Path) -> Dict[str, str]:
    """Loads a snapshot from a JSON file."""
    if not filepath.exists():
        raise FileNotFoundError(f"Snapshot file not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Temporal Echo Recorder: Capture and compare file system snapshots."
    )
    parser.add_argument("command", choices=["snapshot", "compare"],
                        help="Command to execute: 'snapshot' or 'compare'.")
    parser.add_argument("--path", type=Path,
                        help="Path to file or directory for snapshot command.")
    parser.add_argument("--output", type=Path,
                        help="Output file for snapshot (JSON).")
    parser.add_argument("--old-snapshot", type=Path,
                        help="Path to the old snapshot file (JSON) for compare command.")
    parser.add_argument("--new-snapshot", type=Path,
                        help="Path to the new snapshot file (JSON) for compare command.")

    args = parser.parse_args()

    if args.command == "snapshot":
        if not args.path or not args.output:
            parser.error("--path and --output are required for 'snapshot' command.")
        try:
            print(f"Taking snapshot of {args.path}...")
            snapshot = take_snapshot(args.path)
            save_snapshot(snapshot, args.output)
            print(f"Snapshot saved to {args.output}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(1)
    elif args.command == "compare":
        if not args.old_snapshot or not args.new_snapshot:
            parser.error("--old-snapshot and --new-snapshot are required for 'compare' command.")
        try:
            print(f"Loading old snapshot from {args.old_snapshot}...")
            old_snap = load_snapshot(args.old_snapshot)
            print(f"Loading new snapshot from {args.new_snapshot}...")
            new_snap = load_snapshot(args.new_snapshot)

            print("Comparing snapshots...")
            changes = compare_snapshots(old_snap, new_snap)

            print("\n--- Snapshot Comparison Report ---")
            if any(changes.values()):
                for category, files in changes.items():
                    if files:
                        print(f"\n{category.replace('_', ' ').title()}:")
                        for f in files:
                            print(f"  - {f}")
            else:
                print("No changes detected between snapshots.")
            print("----------------------------------")

        except FileNotFoundError as e:
            print(f"Error: {e}")
            exit(1)
        except json.JSONDecodeError:
            print("Error: Invalid JSON snapshot file.")
            exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            exit(1)

if __name__ == "__main__":
    main()
