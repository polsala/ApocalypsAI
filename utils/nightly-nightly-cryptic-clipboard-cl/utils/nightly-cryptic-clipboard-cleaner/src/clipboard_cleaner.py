import sys
import unicodedata
import re


def _replace_common_punctuation(text: str) -> str:
    """Replace a few Unicode punctuation marks with ASCII equivalents.
    This runs *before* ASCII‑only encoding so that characters like em‑dash are kept.
    """
    replacements = {
        "—": "-",  # em dash
        "–": "-",  # en dash
        "‑": "-",  # non‑breaking hyphen
        "\u00A0": " ",  # non‑breaking space
    }
    for src, tgt in replacements.items():
        text = text.replace(src, tgt)
    return text


def clean_clipboard(text: str) -> str:
    """Sanitize clipboard / piped text.

    Steps:
    1. Replace a handful of common Unicode punctuation with ASCII equivalents.
    2. Normalize Unicode to NFKD and drop any remaining non‑ASCII characters.
    3. Collapse any whitespace (spaces, tabs, newlines) to a single space.
    4. Strip leading/trailing whitespace.
    """
    # 1. Preserve simple punctuation
    text = _replace_common_punctuation(text)
    # 2. Unicode normalisation + ASCII‑only encoding
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    # 3. Collapse whitespace
    collapsed = re.sub(r"\s+", " ", ascii_text)
    # 4. Trim
    return collapsed.strip()


def main() -> None:
    """Read from stdin, clean, and print the result."""
    input_text = sys.stdin.read()
    cleaned = clean_clipboard(input_text)
    print(cleaned)


if __name__ == "__main__":
    main()
