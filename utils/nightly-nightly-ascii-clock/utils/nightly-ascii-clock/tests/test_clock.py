import datetime

from utils.nightly-ascii-clock.src.clock import get_ascii_time


def test_ascii_time_fixed():
    """Deterministic test using a fixed datetime.

    # Mock rationale: we directly construct the datetime object instead of
    # patching ``datetime.datetime.now`` to keep the test offline and
    # deterministic.
    """
    fixed_dt = datetime.datetime(2023, 1, 1, 13, 5)  # 13:05
    expected = (
        "  █    ███   ███   ███ \n"
        " ██        █  █   █  █    \n"
        "  █    ███  █   █   ███ \n"
        "  █        █  █   █    █\n"
        " ███   ███   ███   ███ "
    )
    assert get_ascii_time(fixed_dt) == expected
