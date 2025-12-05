"""branch_linter.py

Utility to validate and suggest kebab‑case compliant Git branch names.

Functions
---------
- `is_kebab_case(name: str) -> bool`
- `suggest_kebab_case(name: str) -> str`
- `lint_branch(name: str) -> tuple[bool, str]`
- CLI entry point when run as a module.
"""

import re
import sys
from typing import Tuple

_KEBAB_REGEX = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def is_kebab_case(name: str) -> bool:
    """Return ``True`` if *name* matches kebab‑case.

    Kebab‑case rules for this utility:
    - Only lowercase letters, numbers and hyphens.
    - No leading or trailing hyphens.
    - No consecutive hyphens.
    """
    return bool(_KEBAB_REGEX.fullmatch(name))


def suggest_kebab_case(name: str) -> str:
    """Return a kebab‑case suggestion derived from *name*.

    The algorithm is deliberately simple and deterministic:
    1. Replace any sequence of non‑alphanumeric characters with a single hyphen.
    2. Convert the string to lowercase.
    3. Strip leading/trailing hyphens.
    4. Collapse multiple hyphens into one.
    """
    # Step 1 & 2: replace non‑alnum with hyphen and lower‑case
    interim = re.sub(r"[^A-Za-z0-9]+", "-", name).lower()
    # Step 3: strip leading/trailing hyphens
    interim = interim.strip("-")
    # Step 4: collapse multiple hyphens
    suggestion = re.sub(r"-+", "-", interim)
    return suggestion or "default-branch"


def lint_branch(name: str) -> Tuple[bool, str]:
    """Validate *name* and return ``(is_valid, suggestion)``.

    - If *name* is already kebab‑case, ``suggestion`` is the original name.
    - Otherwise ``suggestion`` is the output of :func:`suggest_kebab_case`.
    """
    if is_kebab_case(name):
        return True, name
    return False, suggest_kebab_case(name)


def _cli() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m branch_linter <branch-name>")
        sys.exit(2)
    branch = sys.argv[1]
    valid, suggestion = lint_branch(branch)
    if valid:
        print("✅ Valid")
        sys.exit(0)
    else:
        print(f"❌ Invalid – suggested: {suggestion}")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
