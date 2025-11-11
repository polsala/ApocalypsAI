import re
import datetime
from typing import Optional


def _unit_to_timedelta(qty: int, unit: str) -> datetime.timedelta:
    """Convert a quantity and unit string to a ``datetime.timedelta``.

    Supported units: seconds, minutes, hours, days, weeks (singular or plural).
    """
    if unit.startswith("second"):
        return datetime.timedelta(seconds=qty)
    if unit.startswith("minute"):
        return datetime.timedelta(minutes=qty)
    if unit.startswith("hour"):
        return datetime.timedelta(hours=qty)
    if unit.startswith("day"):
        return datetime.timedelta(days=qty)
    if unit.startswith("week"):
        return datetime.timedelta(weeks=qty)
    raise ValueError(f"Unsupported unit: {unit}")


def parse_human_time(expr: str, now: Optional[datetime.datetime] = None) -> datetime.datetime:
    """Parse a simple human‑readable time expression.

    Supported patterns (case‑insensitive):
    - ``now``
    - ``in <N> <unit>`` (e.g., ``in 5 minutes``)
    - ``<N> <unit> ago`` (e.g., ``10 seconds ago``)

    ``now`` defaults to ``datetime.datetime.utcnow()`` if not supplied.
    """
    if now is None:
        now = datetime.datetime.utcnow()
    expr = expr.strip().lower()

    if expr == "now":
        return now

    # "in 5 minutes"
    m = re.fullmatch(r"in (\d+) (second|seconds|minute|minutes|hour|hours|day|days|week|weeks)", expr)
    if m:
        qty = int(m.group(1))
        unit = m.group(2)
        delta = _unit_to_timedelta(qty, unit)
        return now + delta

    # "5 minutes ago"
    m = re.fullmatch(r"(\d+) (second|seconds|minute|minutes|hour|hours|day|days|week|weeks) ago", expr)
    if m:
        qty = int(m.group(1))
        unit = m.group(2)
        delta = _unit_to_timedelta(qty, unit)
        return now - delta

    raise ValueError(f"Unsupported expression: {expr}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.parser \"<expression>\"")
        sys.exit(1)
    expression = sys.argv[1]
    try:
        result = parse_human_time(expression)
        print(result.isoformat())
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
