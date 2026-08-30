import sys
import pathlib

# Approximate base image sizes in megabytes (MB)
BASE_IMAGE_SIZES = {
    "python:3.11-slim": 120,
    "alpine:3.18": 5,
    "ubuntu:22.04": 80,
    "node:20-slim": 150,
}

# Heuristic costs per instruction (in MB)
RUN_COST = 5   # per RUN line
COPY_COST = 1  # per COPY or ADD line


def estimate(dockerfile_path: str) -> int:
    """Return an estimated image size (MB) for the given Dockerfile.

    The function reads the Dockerfile line‑by‑line, adds the size of the base
    image (or a default of 100 MB if unknown) and adds a fixed cost for each
    RUN, COPY and ADD instruction.
    """
    path = pathlib.Path(dockerfile_path)
    if not path.is_file():
        raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")

    total = 0
    with path.open() as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            parts = stripped.split()
            instr = parts[0].upper()
            if instr == "FROM":
                base = parts[1]
                total += BASE_IMAGE_SIZES.get(base, 100)  # default 100 MB
            elif instr == "RUN":
                total += RUN_COST
            elif instr in ("COPY", "ADD"):
                total += COPY_COST
    return total


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.size_estimator <Dockerfile>")
        sys.exit(1)
    dockerfile = sys.argv[1]
    try:
        size = estimate(dockerfile)
        print(f"Estimated image size: {size} MB")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
