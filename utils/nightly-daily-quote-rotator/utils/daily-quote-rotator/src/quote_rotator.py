import json
import pathlib
import datetime
import sys
from typing import List


class QuoteRotator:
    """Cycle through a list of quotes, returning a new one each calendar day.

    The rotation state is stored in a JSON file containing the last date a quote
    was served and the index of that quote in the list.
    """

    def __init__(self, quotes_path: pathlib.Path, state_path: pathlib.Path):
        self.quotes_path = quotes_path
        self.state_path = state_path
        self.quotes: List[str] = self._load_quotes()
        self.state = self._load_state()

    def _load_quotes(self) -> List[str]:
        """Read quotes from ``quotes.txt`` – one per non‑empty line."""
        raw = self.quotes_path.read_text(encoding="utf-8")
        return [line.strip() for line in raw.splitlines() if line.strip()]

    def _load_state(self) -> dict:
        """Load persisted state or start fresh if the file is missing/corrupt."""
        if self.state_path.exists():
            try:
                return json.loads(self.state_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                # Mock rationale: corrupted state should not crash the utility.
                return {}
        return {}

    def _save_state(self) -> None:
        """Write the current state back to ``state.json``."""
        self.state_path.write_text(json.dumps(self.state), encoding="utf-8")

    def get_today_quote(self, today: datetime.date = None) -> str:
        """Return the quote for *today*.

        If the stored date differs from ``today`` the index is advanced (wrapping
        around the quote list) and the state is persisted.
        """
        today = today or datetime.date.today()
        last_date_str = self.state.get("date")
        idx = self.state.get("index", 0)

        if last_date_str != today.isoformat():
            # Advance to the next quote only once per day.
            idx = (idx + 1) % len(self.quotes) if self.quotes else 0
            self.state["date"] = today.isoformat()
            self.state["index"] = idx
            self._save_state()
        return self.quotes[idx] if self.quotes else "No quotes available."


def main() -> None:
    base_dir = pathlib.Path(__file__).resolve().parents[1]
    quotes_path = base_dir / "quotes.txt"
    state_path = base_dir / "state.json"
    rotator = QuoteRotator(quotes_path, state_path)
    print(rotator.get_today_quote())


if __name__ == "__main__":
    main()
