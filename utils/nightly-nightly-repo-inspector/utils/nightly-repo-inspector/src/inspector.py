import argparse
import json
import os
from pathlib import Path
from typing import Dict, Any


def inspect_path(root: Path) -> Dict[str, Any]:
    """Recursively inspect *root* and return a summary.

    The returned dictionary has the shape:
    {
        "total_files": int,
        "total_size": int,  # bytes
        "extensions": {
            ".py": {"count": int, "size": int},
            ".txt": {"count": int, "size": int},
            ...
        }
    }
    """
    total_files = 0
    total_size = 0
    extensions: Dict[str, Dict[str, int]] = {}

    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            file_path = Path(dirpath) / fname
            try:
                size = file_path.stat().st_size
            except OSError:
                # Skip files we cannot access
                continue
            ext = file_path.suffix.lower() or "<no-ext>"
            total_files += 1
            total_size += size
            if ext not in extensions:
                extensions[ext] = {"count": 0, "size": 0}
            extensions[ext]["count"] += 1
            extensions[ext]["size"] += size

    return {
        "total_files": total_files,
        "total_size": total_size,
        "extensions": extensions,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a directory and output a JSON summary.")
    parser.add_argument("path", type=Path, help="Path to the directory to inspect")
    args = parser.parse_args()

    if not args.path.is_dir():
        parser.error(f"{args.path} is not a directory")

    summary = inspect_path(args.path)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
