import builtins
import importlib
import types
from unittest import mock

# Mock rationale: we replace random.choice to return a deterministic element so the test is repeatable offline.

def test_get_compliment_returns_expected_when_random_is_mocked():
    # Dynamically import the module under test
    random_compliment = importlib.import_module('random_compliment')

    with mock.patch('random.choice', return_value='You are a coding wizard!'):
        result = random_compliment.get_compliment()
        assert result == 'You are a coding wizard!'

def test_cli_prints_compliment(capsys):
    random_compliment = importlib.import_module('random_compliment')
    with mock.patch('random.choice', return_value='Your logic is as clear as crystal.'):
        # Simulate running the module as a script
        random_compliment._main()
        captured = capsys.readouterr()
        assert captured.out.strip() == 'Your logic is as clear as crystal.'
