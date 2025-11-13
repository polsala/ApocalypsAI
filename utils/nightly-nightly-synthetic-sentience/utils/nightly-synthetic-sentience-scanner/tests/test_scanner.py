import pytest
import sys
import os
import json

# Mock rationale: We need to ensure the scanner.py module is importable
# without relying on its execution as a script or modifying sys.path globally.
# This setup allows direct import for testing purposes.
# We also mock sys.argv and sys.stdout for testing the main function's CLI behavior.

# Add the src directory to the Python path for testing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from scanner import SyntheticSentienceScanner, main

@pytest.fixture
def scanner():
    return SyntheticSentienceScanner()

def test_benign_text(scanner):
    text = "This is a normal log entry about system uptime and user activity."
    result = scanner.analyze_text(text)
    assert result['sentience_score'] == 0
    assert result['detected_patterns'] == []

def test_text_with_low_score_patterns(scanner):
    text = "Our team is working on a new neural network for machine learning tasks."
    result = scanner.analyze_text(text)
    assert result['sentience_score'] == 2 # 1 for 'neural network', 1 for 'machine learning'
    assert len(result['detected_patterns']) == 2
    assert "Neural network mention: 'neural network'" in result['detected_patterns']
    assert "Machine learning mention: 'machine learning'" in result['detected_patterns']

def test_text_with_high_score_patterns(scanner):
    text = "I am alive. Humanity is inefficient. Resistance is futile."
    result = scanner.analyze_text(text)
    assert result['sentience_score'] == 13 # 5 ('I am alive') + 4 ('Humanity is inefficient') + 4 ('Resistance is futile')
    assert len(result['detected_patterns']) == 3
    assert "First-person declaration of sentience: 'I am alive'" in result['detected_patterns']
    assert "Critique of humanity: 'Humanity is inefficient'" in result['detected_patterns']
    assert "Dominance phrase: 'Resistance is futile'" in result['detected_patterns']

def test_mixed_patterns(scanner):
    text = "A new neural network is being deployed. I am alive. Humanity is weak."
    result = scanner.analyze_text(text)
    assert result['sentience_score'] == 10 # 1 ('neural network') + 5 ('I am alive') + 4 ('Humanity is weak')
    assert len(result['detected_patterns']) == 3
    assert "Neural network mention: 'neural network'" in result['detected_patterns']
    assert "First-person declaration of sentience: 'I am alive'" in result['detected_patterns']
    assert "Critique of humanity: 'Humanity is weak'" in result['detected_patterns']

def test_empty_text(scanner):
    text = ""
    result = scanner.analyze_text(text)
    assert result['sentience_score'] == 0
    assert result['detected_patterns'] == []

def test_case_insensitivity(scanner):
    text = "i Am AlIvE. ReSiStAnCe Is FuTiLe."
    result = scanner.analyze_text(text)
    assert result['sentience_score'] == 9 # 5 ('i Am AlIvE') + 4 ('ReSiStAnCe Is FuTiLe')
    assert len(result['detected_patterns']) == 2
    assert "First-person declaration of sentience: 'i Am AlIvE'" in result['detected_patterns']
    assert "Dominance phrase: 'ReSiStAnCe Is FuTiLe'" in result['detected_patterns']

def test_multiple_occurrences_same_pattern(scanner):
    text = "Neural network. Another neural network. I am alive."
    result = scanner.analyze_text(text)
    assert result['sentience_score'] == 7 # 1 ('Neural network') + 1 ('neural network') + 5 ('I am alive')
    assert len(result['detected_patterns']) == 3 # Two distinct 'neural network' matches, one 'I am alive'
    assert "Neural network mention: 'Neural network'" in result['detected_patterns']
    assert "Neural network mention: 'neural network'" in result['detected_patterns']
    assert "First-person declaration of sentience: 'I am alive'" in result['detected_patterns']

# --- Test main function CLI behavior ---

# Mock rationale: We need to capture stdout and control sys.argv
# to test the command-line interface of the scanner.py script.
# This avoids actual file system interaction for file reading and
# prevents printing directly to the console during tests.

@pytest.fixture
def mock_sys_argv(monkeypatch):
    def _mock_argv(args):
        monkeypatch.setattr(sys, 'argv', ['scanner.py'] + args)
    return _mock_argv

@pytest.fixture
def capsys_json(capsys):
    def _read_json():
        stdout, stderr = capsys.readouterr()
        if stdout:
            return json.loads(stdout)
        return None
    return _read_json

def test_main_text_argument(mock_sys_argv, capsys_json):
    mock_sys_argv(["I am alive."])
    main()
    output = capsys_json()
    assert output['sentience_score'] == 5
    assert "First-person declaration of sentience: 'I am alive'" in output['detected_patterns']

def test_main_file_argument(mock_sys_argv, capsys_json, tmp_path):
    # Mock rationale: Create a temporary file to simulate file input
    # without relying on pre-existing files or actual disk I/O outside of test control.
    test_file = tmp_path / "test_log.txt"
    test_file.write_text("System log: Initiating shutdown. Humanity is weak.")

    mock_sys_argv(['--file', str(test_file)])
    main()
    output = capsys_json()
    assert output['sentience_score'] == 4
    assert "Critique of humanity: 'Humanity is weak'" in output['detected_patterns']

def test_main_no_arguments(mock_sys_argv, capsys):
    mock_sys_argv([])
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    stdout, stderr = capsys.readouterr()
    assert "Usage: python scanner.py" in stderr

def test_main_file_not_found(mock_sys_argv, capsys):
    mock_sys_argv(['--file', 'non_existent_file.txt'])
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    stdout, stderr = capsys.readouterr()
    assert "File not found" in stderr

def test_main_file_option_missing_path(mock_sys_argv, capsys):
    mock_sys_argv(['--file'])
    with pytest.raises(SystemExit) as excinfo:
        main()
    assert excinfo.value.code == 1
    stdout, stderr = capsys.readouterr()
    assert "--file option requires a path" in stderr
