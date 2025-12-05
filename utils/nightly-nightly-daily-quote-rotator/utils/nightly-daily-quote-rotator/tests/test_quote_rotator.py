import datetime
from unittest import mock

# Import the module under test
from quote_rotator import get_quote, main


def test_get_quote_deterministic_fixed_date():
    """Given a known date, the function must return the expected quote.

    The expected quote is calculated manually using the same algorithm.
    """
    test_date = datetime.date(2023, 1, 1)  # ordinal = 738156
    expected_index = test_date.toordinal() % 10  # len(_QUOTES) == 10
    # The list of quotes is defined in the module; we replicate the first few entries.
    expected_quotes = [
        "The early bird gets the worm, but the second mouse gets the cheese.",
        "When life gives you lemons, make lemonade… then find someone whose life gave them vodka.",
        "I’m not lazy, I’m on energy‑saving mode.",
        "If at first you don’t succeed, skydiving is not for you.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "To err is human; to really mess things up you need a computer.",
        "I would tell you a UDP joke, but you might not get it.",
        "Debugging: Removing the needles from the haystack.",
        "There are 10 types of people: those who understand binary and those who don’t.",
        "In a world full of APIs, be a RESTful endpoint.",
    ]
    assert get_quote(test_date) == expected_quotes[expected_index]


def test_get_quote_uses_today_when_no_date_provided():
    """When *target_date* is ``None`` the function should call ``datetime.date.today``.

    We mock ``datetime.date.today`` to return a fixed date and verify the output.
    """
    fixed_today = datetime.date(2025, 11, 29)
    with mock.patch.object(datetime.date, "today", return_value=fixed_today):
        # Mock rationale: isolate external date source.
        quote = get_quote()
    expected_index = fixed_today.toordinal() % 10
    # Re‑use the same quote list as above (duplicate for clarity).
    expected_quotes = [
        "The early bird gets the worm, but the second mouse gets the cheese.",
        "When life gives you lemons, make lemonade… then find someone whose life gave them vodka.",
        "I’m not lazy, I’m on energy‑saving mode.",
        "If at first you don’t succeed, skydiving is not for you.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "To err is human; to really mess things up you need a computer.",
        "I would tell you a UDP joke, but you might not get it.",
        "Debugging: Removing the needles from the haystack.",
        "There are 10 types of people: those who understand binary and those who don’t.",
        "In a world full of APIs, be a RESTful endpoint.",
    ]
    assert quote == expected_quotes[expected_index]


def test_cli_prints_quote(capsys):
    """The CLI should print the quote for the supplied ``--date`` argument.

    We invoke ``main`` with a known date and capture stdout.
    """
    test_date_str = "2024-02-29"
    # Expected quote calculation
    test_date = datetime.datetime.strptime(test_date_str, "%Y-%m-%d").date()
    expected_quote = get_quote(test_date)
    # Run the CLI entry point
    main(["--date", test_date_str])
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_quote
