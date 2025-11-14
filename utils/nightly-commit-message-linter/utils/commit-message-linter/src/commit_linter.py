import re
import sys
from typing import List

# Allowed commit types according to Conventional Commits
ALLOWED_TYPES = {
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
}

# Regex for the Conventional Commits header
HEADER_REGEX = re.compile(
    r"^(?P<type>\w+)(\((?P<scope>[^)]+)\))?: (?P<description>.+)$"
)


def lint_message(message: str) -> List[str]:
    """Validate a commit message.

    Returns a list of human‑readable issue strings. An empty list means the
    message complies with the Conventional Commits spec.
    """
    issues: List[str] = []
    # Split into lines; only the first line (header) is validated here.
    lines = message.strip().splitlines()
    if not lines:
        issues.append("Commit message is empty.")
        return issues

    header = lines[0]
    if len(header) > 72:
        issues.append(
            f"Header exceeds 72 characters ({len(header)})."
        )

    match = HEADER_REGEX.match(header)
    if not match:
        issues.append(
            "Header does not match '<type>(<scope>): <description>' pattern."
        )
    else:
        commit_type = match.group("type")
        if commit_type not in ALLOWED_TYPES:
            issues.append(
                f"Commit type '{commit_type}' is not allowed. Allowed types: {', '.join(sorted(ALLOWED_TYPES))}."
            )
        # Scope is optional; no further validation needed.
        description = match.group("description")
        if not description.strip():
            issues.append("Description part of the header is empty.")

    return issues


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m commit_linter \"<commit message>\"")
        sys.exit(1)
    message = sys.argv[1]
    issues = lint_message(message)
    for issue in issues:
        print(issue)
    # Exit code 0 if no issues, 1 otherwise
    sys.exit(0 if not issues else 1)


if __name__ == "__main__":
    main()
