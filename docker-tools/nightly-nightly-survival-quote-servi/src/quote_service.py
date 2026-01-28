import datetime\n\n_QUOTES = [\n    "Never trust a calm sky in the wasteland.",\n    "When the wind howls, listen for the whisper of supplies.",\n    "A rusted can opener is worth more than a golden sword.",\n    "Water is the true currency of the apocalypse.",\n    "Even a broken compass points somewhere useful.\n]\n\ndef get_quote(for_date: datetime.date) -> str:\n    """Return a deterministic quote based on *for_date*.
\n    The algorithm is simple: compute the ordinal of the date and use it
    modulo the number of available quotes. This guarantees that the same
    date always yields the same quote without any external state.
    """\n    index = for_date.toordinal() % len(_QUOTES)\n    return _QUOTES[index]\n
