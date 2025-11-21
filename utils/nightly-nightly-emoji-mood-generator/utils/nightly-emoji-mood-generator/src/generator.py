import sys
from pathlib import Path
from typing import List

POSITIVE_WORDS = {"add", "fix", "improve", "refactor", "optimize", "success", "enable", "upgrade"}
NEGATIVE_WORDS = {"bug", "fail", "error", "break", "deprecate", "remove", "slow"}

EMOJI_MAP = [
    (-float('inf'), -5, "😞"),   # very negative
    (-5, -1, "🙁"),            # negative
    (-1, 1, "😐"),             # neutral
    (1, 5, "🙂"),              # positive
    (5, float('inf'), "😄"),   # very positive
]

def score_message(message: str) -> int:
    """Simple heuristic: +1 for each positive word, -1 for each negative word.
    Case‑insensitive, whole‑word matching.
    """
    words = {w.strip('.,!?:;').lower() for w in message.split()}
    score = 0
    for w in words:
        if w in POSITIVE_WORDS:
            score += 1
        if w in NEGATIVE_WORDS:
            score -= 1
    return score

def aggregate_score(messages: List[str]) -> int:
    """Sum the scores of all messages."""
    return sum(score_message(m) for m in messages)

def map_score_to_emoji(total: int) -> str:
    """Map the aggregate score to an emoji based on EMOJI_MAP ranges."""
    for low, high, emoji in EMOJI_MAP:
        if low < total <= high:
            return emoji
    # Fallback (should never happen)
    return "🤔"

def generate_mood_emoji(messages: List[str]) -> str:
    """Public API: given a list of commit messages, return the mood emoji."""
    total = aggregate_score(messages)
    return map_score_to_emoji(total)

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python -m nightly_emoji_mood_generator <commit_messages_file>")
        sys.exit(1)
    file_path = Path(sys.argv[1])
    if not file_path.is_file():
        print(f"File not found: {file_path}")
        sys.exit(1)
    messages = [line.strip() for line in file_path.read_text().splitlines() if line.strip()]
    emoji = generate_mood_emoji(messages)
    print(emoji)

if __name__ == "__main__":
    main()
