import json
import random
import pathlib
import sys


def load_quotes(path: pathlib.Path) -> list[str]:
    """Load quotes from a JSON file.

    Args:
        path: Path to a JSON file containing a list of strings.

    Returns:
        A list of quote strings.

    Raises:
        ValueError: If the JSON does not contain a list.
    """
    with path.open('r', encoding='utf-8') as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("Quotes JSON must be a list of strings")
    return data


def get_random_quote(quotes_path: pathlib.Path | None = None) -> str:
    """Return a random quote from the bundled list.

    If *quotes_path* is ``None`` the function looks for ``quotes.json`` in the
    same directory as this file.
    """
    if quotes_path is None:
        quotes_path = pathlib.Path(__file__).with_name('quotes.json')
    quotes = load_quotes(quotes_path)
    return random.choice(quotes)


def main() -> None:
    try:
        quote = get_random_quote()
        print(quote)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
