import argparse
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Quote:
    text: str
    theme: str


class QuoteGenerator:
    """Provides random Zen quotes, optionally filtered by theme."""

    _quotes: List[Quote] = (
        Quote(text="The journey of a thousand miles begins with a single step.", theme="growth"),
        Quote(text="When you realize nothing is lacking, the whole world belongs to you.", theme="mindfulness"),
        Quote(text="A jug fills drop by drop; patience is the silent river.", theme="patience"),
        Quote(text="Even a silent stone can echo wisdom.", theme="humor"),
        Quote(text="The moon does not argue with the night; it simply shines.", theme="mindfulness"),
        Quote(text="If you chase two rabbits, you will catch none.", theme="focus"),
        Quote(text="A single breath can calm a storm inside.", theme="mindfulness"),
        Quote(text="Growth is a garden; water it daily.", theme="growth"),
    )

    def get_random_quote(self, theme: Optional[str] = None) -> Quote:
        """Return a random Quote.

        If *theme* is provided, only quotes matching that theme are considered.
        Raises *ValueError* if no quotes match the requested theme.
        """
        eligible = [q for q in self._quotes if theme is None or q.theme == theme]
        if not eligible:
            raise ValueError(f"No quotes found for theme '{theme}'.")
        # Random choice – deterministic in tests via mocking.
        return random.choice(eligible)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print a random Zen quote.")
    parser.add_argument(
        "--theme",
        type=str,
        help="Optional theme to filter quotes (e.g., mindfulness, growth).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    generator = QuoteGenerator()
    try:
        quote = generator.get_random_quote(theme=args.theme)
        print(f"\u201C{quote.text}\u201D — {quote.theme.title()}")
    except ValueError as exc:
        print(exc)


if __name__ == "__main__":
    main()
