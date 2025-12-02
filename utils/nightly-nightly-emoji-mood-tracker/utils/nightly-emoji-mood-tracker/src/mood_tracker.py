import json
import os
from collections import Counter
from datetime import datetime, timedelta
from typing import Dict, Optional


class MoodTracker:
    """Simple emoji‑based mood logger.

    The data is stored as a JSON object mapping ISO dates to emoji strings:
    {
        "2025-12-01": "😄",
        "2025-12-02": "😐",
        ...
    }
    """

    def __init__(self, log_path: str = "mood_log.json") -> None:
        self.log_path = log_path
        # Ensure the file exists and contains a dict
        if not os.path.exists(self.log_path):
            self._write_log({})
        else:
            # Validate existing content (mock rationale: keep it simple)
            try:
                data = self._read_log()
                if not isinstance(data, dict):
                    raise ValueError("Log file corrupted: not a dict")
            except json.JSONDecodeError as exc:
                raise ValueError(f"Log file corrupted: {exc}") from exc

    def _read_log(self) -> Dict[str, str]:
        with open(self.log_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_log(self, data: Dict[str, str]) -> None:
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_entry(self, date: str, emoji: str) -> None:
        """Add or overwrite a mood entry for *date*.

        Args:
            date: ISO formatted date string (YYYY‑MM‑DD).
            emoji: Any emoji character representing the mood.
        """
        # Basic validation (mock rationale: keep lightweight)
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("date must be in YYYY-MM-DD format") from exc
        if not emoji:
            raise ValueError("emoji must be a non‑empty string")

        data = self._read_log()
        data[date] = emoji
        self._write_log(data)

    def get_summary(self, days: int = 30) -> Dict[str, Optional[object]]:
        """Return mood statistics for the last *days* days.

        The summary includes total entries, per‑emoji counts, and the most common emoji.
        """
        if days <= 0:
            raise ValueError("days must be positive")
        cutoff = datetime.utcnow().date() - timedelta(days=days)
        data = self._read_log()
        recent_emojis = [emoji for d, emoji in data.items() if datetime.strptime(d, "%Y-%m-%d").date() >= cutoff]
        counts = Counter(recent_emojis)
        most_common = counts.most_common(1)[0][0] if counts else None
        return {
            "total_entries": len(recent_emojis),
            "counts": dict(counts),
            "most_common": most_common,
        }

# If executed as a script, provide a tiny demo (not used in tests)
if __name__ == "__main__":
    tracker = MoodTracker()
    today = datetime.utcnow().strftime("%Y-%m-%d")
    tracker.add_entry(today, "😄")
    print(tracker.get_summary())
