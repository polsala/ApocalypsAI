"""Zen Garden Scheduler utility.

Provides `generate_schedule` to turn a config dict into a list of
human‑readable schedule lines. Also offers a CLI entry point.
"""

from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path
from typing import List, Mapping

try:
    import yaml  # optional
except ImportError:  # pragma: no cover
    yaml = None


def _parse_config_file(path: Path) -> Mapping:
    """Load YAML or JSON config from *path*.

    # Mock rationale:
    The function is isolated; in tests we bypass file I/O.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")
    text = path.read_text(encoding="utf-8")
    if yaml:
        return yaml.safe_load(text)
    # Fallback to JSON if yaml not available
    import json

    return json.loads(text)


def generate_schedule(config: Mapping, start_time: datetime.time = datetime.time(9, 0)) -> List[str]:
    """Generate a schedule from *config*.

    *config* must contain an ``activities`` key with a list of mappings,
    each having ``name`` (str) and ``duration`` (int, minutes).

    Returns a list of strings like ``09:00 - 09:15: Meditation``.
    """
    activities = config.get("activities", [])
    if not isinstance(activities, list):
        raise ValueError("`activities` must be a list")
    schedule = []
    current = datetime.datetime.combine(datetime.date.today(), start_time)
    for act in activities:
        name = act.get("name")
        duration = act.get("duration")
        if not isinstance(name, str) or not isinstance(duration, int):
            raise ValueError("Each activity needs a string `name` and int `duration`")
        end = current + datetime.timedelta(minutes=duration)
        line = f"{current.time().strftime('%H:%M')} - {end.time().strftime('%H:%M')}: {name}"
        schedule.append(line)
        current = end
    return schedule


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a calming daily schedule.")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to YAML (or JSON) configuration file.",
    )
    args = parser.parse_args(argv)

    try:
        cfg = _parse_config_file(args.config)
        schedule = generate_schedule(cfg)
        for line in schedule:
            print(line)
        return 0
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
