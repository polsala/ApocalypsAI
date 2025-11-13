'''Daily Zen Quote Generator.

Provides a deterministic quote based on the supplied date.
'''\n\nimport sys\nimport datetime\nfrom typing import List\n\n_QUOTES: List[str] = [\
    "The journey of a thousand miles begins with one step.",\
    "Simplicity is the ultimate sophistication.",\
    "When the mind is still, the universe surrenders.",\
    "The obstacle is the path.",\
    "Let go or be dragged.",\
    "Silence is a source of great strength.",\
    "Be present, not perfect.",\
    "All is water.",\
]\n\n\ndef get_zen_quote(date: datetime.date) -> str:\n    """Return a deterministic Zen quote for the given date."""\n    # Use YYYYMMDD integer modulo number of quotes\n    index = int(date.strftime("%Y%m%d")) % len(_QUOTES)\n    return _QUOTES[index]\n\n\ndef main(argv: List[str] | None = None) -> int:\n    """CLI entry point.\n\n    Usage:\n        python -m utils.daily-zen-quote-generator.src.main [YYYY-MM-DD]\n\n    If no date is provided, uses today's date.\n    """\n    if argv is None:\n        argv = sys.argv[1:]\n\n    if len(argv) > 1:\n        print("Too many arguments. Provide at most one date in YYYY-MM-DD format.", file=sys.stderr)\n        return 1\n\n    if argv:\n        try:\n            target_date = datetime.datetime.strptime(argv[0], "%Y-%m-%d").date()\n        except ValueError:\n            print("Invalid date format. Use YYYY-MM-DD.", file=sys.stderr)\n            return 1\n    else:\n        target_date = datetime.date.today()\n\n    quote = get_zen_quote(target_date)\n    print(quote)\n    return 0\n\n\nif __name__ == "__main__":\n    sys.exit(main())
