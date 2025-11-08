'''Daily Zen Quote Generator.

Provides a deterministic quote based on the current date.
No external network calls; all data is embedded.
'''\n\nfrom __future__ import annotations\n\nimport argparse\nimport datetime\nimport sys\nfrom typing import List\n\n_QUOTES: List[str] = [\n    "The journey of a thousand miles begins with one step.",\n    "When the mind is still, the universe surrenders.",\n    "Simplicity is the ultimate sophistication.",\n    "The obstacle is the path.",\n    "Let go or be dragged.",\n    "In the middle of difficulty lies opportunity.",\n    "Silence is a source of great strength.",\n    "Be like water.",\n    "All that we are is the result of what we have thought.",\n    "The only constant is change.",\n]\n\n\ndef get_today_quote(date: datetime.date | None = None) -> str:\n    """Return the quote for *date* (defaults to today).\n\n    The selection is deterministic: ``ordinal % len(_QUOTES)``.\n    """\n    if date is None:\n        date = datetime.date.today()\n    index = date.toordinal() % len(_QUOTES)\n    return _QUOTES[index]\n\n\ndef main(argv: List[str] | None = None) -> int:\n    parser = argparse.ArgumentParser(
        prog="daily-zen-quote",
        description="Print a deterministic Zen quote for the current day."
    )\n    parser.parse_args(argv)  # No extra options needed\n    quote = get_today_quote()\n    print(quote)\n    return 0\n\n\nif __name__ == "__main__":\n    sys.exit(main())
