import argparse
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Quote:
    text: str
    tags: List[str]

# Built‑in quote pool – whimsical yet inspirational
_QUOTE_POOL: List[Quote] = [
    Quote(text="The journey of a thousand miles begins with a single step.", tags=["mindfulness", "motivation"]),
    Quote(text="When you realize nothing is lacking, the whole world belongs to you.", tags=["philosophy"]),
    Quote(text="A cup of tea is a cup of peace.", tags=["humor", "mindfulness"]),
    Quote(text="Silence is the language of the soul.", tags=["spiritual"]),
    Quote(text="If you cannot find the sunshine, be the sunshine.", tags=["motivation", "humor"]),
]


def _filter_by_tag(quotes: List[Quote], tag: Optional[str]) -> List[Quote]:
    if tag is None:
        return quotes
    return [q for q in quotes if tag.lower() in (t.lower() for t in q.tags)]


def get_random_quote(tag: Optional[str] = None) -> Quote:
    """Return a random Quote, optionally limited to those containing *tag*.

    Raises:
        ValueError: If no quotes match the supplied tag.
    """
    filtered = _filter_by_tag(_QUOTE_POOL, tag)
    if not filtered:
        raise ValueError(f"No quotes found for tag '{tag}'.")
    return random.choice(filtered)


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--tag",
        type=str,
        help="Optional tag to filter quotes (e.g., mindfulness, humor).",
    )
    args = parser.parse_args()
    try:
        quote = get_random_quote(args.tag)
        print(f"\"{quote.text}\"")
        if quote.tags:
            print(f"  — tags: {', '.join(quote.tags)}")
    except ValueError as e:
        parser.error(str(e))


if __name__ == "__main__":
    _cli()
