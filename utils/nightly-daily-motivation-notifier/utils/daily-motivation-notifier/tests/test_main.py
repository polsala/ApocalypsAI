import os
import sys
from unittest import mock

# Mock rationale: Ensure deterministic output by fixing random.choice.

def _load_module():
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    import main
    return main

def test_get_random_quote_deterministic():
    main = _load_module()
    with mock.patch('random.choice', return_value=main._QUOTES[0]):
        assert main.get_random_quote() == main._QUOTES[0]

def test_main_prints_quote(capsys):
    main = _load_module()
    # Mock rationale: Force get_random_quote to return a known value.
    with mock.patch.object(main, 'get_random_quote', return_value=main._QUOTES[2]):
        main.main()
        captured = capsys.readouterr()
        assert captured.out.strip() == main._QUOTES[2]
