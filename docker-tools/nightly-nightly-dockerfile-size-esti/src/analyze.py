import sys
import os
from typing import Dict

# Simple lookup for common base images (size in MB)
BASE_IMAGE_SIZES: Dict[str, int] = {
    "python:3.11-slim": 30,
    "alpine": 5,
    "ubuntu:20.04": 70,
}

DEFAULT_BASE_SIZE = 20  # MB, used when image not in lookup

def _parse_dockerfile(path: str) -> Dict[str, int]:
    """Parse Dockerfile and count instruction types.

    Returns a dict with keys: 'run', 'copy_add', 'base_image'.
    """
    run_cnt = 0
    copy_add_cnt = 0
    base_image = None
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            tokens = line.split()
            instr = tokens[0].upper()
            if instr == "FROM" and len(tokens) >= 2:
                base_image = tokens[1].lower()
            elif instr == "RUN":
                run_cnt += 1
            elif instr in ("COPY", "ADD"):
                copy_add_cnt += 1
    return {"run": run_cnt, "copy_add": copy_add_cnt, "base_image": base_image}

def _base_image_size(image_name: str | None) -> int:
    if not image_name:
        return DEFAULT_BASE_SIZE
    return BASE_IMAGE_SIZES.get(image_name, DEFAULT_BASE_SIZE)

def estimate_size(dockerfile_path: str) -> int:
    """Estimate Docker image size (in MB) using simple heuristics.

    Heuristics:
    * Base image size from lookup (default 20 MB).
    * Each RUN instruction adds ~50 MB.
    * Each COPY or ADD adds ~5 MB.
    """
    if not os.path.isfile(dockerfile_path):
        raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")
    stats = _parse_dockerfile(dockerfile_path)
    size = _base_image_size(stats["base_image"]) + stats["run"] * 50 + stats["copy_add"] * 5
    return size

def _cli():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "Dockerfile"
    try:
        size = estimate_size(path)
        print(f"Estimated image size: {size} MB")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    _cli()
