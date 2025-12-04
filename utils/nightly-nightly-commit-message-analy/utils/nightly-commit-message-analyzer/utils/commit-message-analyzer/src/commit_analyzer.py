import re
from typing import Dict, List, Any, Optional

# Conventional commit types as per spec
CONVENTIONAL_TYPES = {
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

# Regex to capture type, optional scope, and subject
HEADER_RE = re.compile(
    r"^(?P<type>\w+)"  # type
    r"(?P<scope>\([^\)]+\))?"  # optional scope
    r":\s(?P<subject>.+)$"
)

# Footer pattern: key: value
FOOTER_RE = re.compile(r"^(?P<key>[^:]+):\s(?P<value>.+)$")


def _parse_header(line: str) -> Optional[Dict[str, str]]:
    """Parse the header line of a Conventional Commit.

    Returns a dict with keys: type, scope, subject or None if not matched.
    """
    match = HEADER_RE.match(line)
    if not match:
        return None
    return {
        "type": match.group("type"),
        "scope": match.group("scope"),
        "subject": match.group("subject"),
    }


def _parse_footers(lines: List[str]) -> Dict[str, str]:
    """Parse footer lines into a key/value dict."""
    footers = {}
    for line in lines:
        match = FOOTER_RE.match(line)
        if match:
            key = match.group("key").strip()
            value = match.group("value").strip()
            footers[key] = value
    return footers


def analyze(message: str) -> Dict[str, Any]:
    """Validate and parse a commit message.

    Parameters
    ----------
    message: str
        The raw commit message.

    Returns
    -------
    dict
        Structured representation with validation status and components.
    """
    result: Dict[str, Any] = {
        "is_valid": True,
        "type": None,
        "scope": None,
        "subject": None,
        "body": [],
        "footers": {},
        "errors": [],
    }

    if not message:
        result["is_valid"] = False
        result["errors"].append("Commit message is empty.")
        return result

    # Split into lines, preserve order
    lines = message.splitlines()
    header_line = lines[0].strip()
    header = _parse_header(header_line)
    if not header:
        result["is_valid"] = False
        result["errors"].append("Header does not match Conventional Commit format.")
        return result

    # Validate type
    if header["type"] not in CONVENTIONAL_TYPES:
        result["is_valid"] = False
        result["errors"].append(f"Unknown commit type '{header['type']}'.")

    # Validate subject presence
    if not header["subject"]:
        result["is_valid"] = False
        result["errors"].append("Subject is missing.")

    result["type"] = header["type"]
    result["scope"] = header["scope"]
    result["subject"] = header["subject"]

    # Body and footers: split by first blank line
    body_lines: List[str] = []
    footer_lines: List[str] = []
    blank_found = False
    for line in lines[1:]:
        if not line.strip() and not blank_found:
            blank_found = True
            continue
        if blank_found:
            footer_lines.append(line)
        else:
            body_lines.append(line)

    result["body"] = [l for l in body_lines if l.strip()]
    result["footers"] = _parse_footers(footer_lines)

    return result
