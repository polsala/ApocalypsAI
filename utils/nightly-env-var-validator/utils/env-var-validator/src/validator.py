#!/usr/bin/env python3
"""env-var-validator

A tiny command‑line utility that validates required keys in a .env file.

Usage:
    python -m env_var_validator --env-file .env --required KEY1,KEY2
"""

import argparse
import json
import os
import sys
from typing import List, Set


def _load_env_file(path: str) -> Set[str]:
    """Parse a .env file and return a set of defined variable names.

    Empty lines and comments (starting with '#') are ignored.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Env file not found: {path}")
    keys: Set[str] = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue  # malformed line – ignore for robustness
            key, _ = line.split("=", 1)
            keys.add(key.strip())
    return keys


def validate(env_path: str, required: List[str]) -> List[str]:
    """Return a list of missing required keys.

    Parameters
    ----------
    env_path: str
        Path to the .env file.
    required: List[str]
        List of required variable names.
    """
    try:
        present = _load_env_file(env_path)
    except FileNotFoundError as exc:
        raise exc
    missing = [key for key in required if key not in present]
    return missing


def _parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate required keys in a .env file.")
    parser.add_argument(
        "--env-file",
        required=True,
        help="Path to the .env file to validate.",
    )
    parser.add_argument(
        "--required",
        required=True,
        help="Comma‑separated list of required environment variable names.",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    try:
        args = _parse_args(argv)
        required_keys = [key.strip() for key in args.required.split(",") if key.strip()]
        missing = validate(args.env_file, required_keys)
        result = {"missing": missing}
        print(json.dumps(result))
        return 0 if not missing else 1
    except FileNotFoundError as e:
        sys.stderr.write(str(e) + "\n")
        return 2
    except Exception as e:  # pragma: no cover – unexpected errors
        sys.stderr.write(f"Unexpected error: {e}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
