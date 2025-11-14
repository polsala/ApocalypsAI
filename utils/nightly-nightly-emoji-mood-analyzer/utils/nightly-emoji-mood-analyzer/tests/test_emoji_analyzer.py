import json
from src import emoji_analyzer

# Mock rationale: All test data is hard‑coded; no external I/O or network calls.

def test_extract_emojis_simple():
    text = "Hello 😀 world 🌍!"
    emojis = emoji_analyzer.extract_emojis(text)
    assert emojis == ["😀", "🌍"]

def test_analyze_emojis_counts():
    messages = [
        "Good morning! ☀️",
        "I love pizza 🍕🍕",
        "Feeling sad 😢",
        "Party time! 🎉🎉🎉",
        "No emojis here",
    ]
    result = emoji_analyzer.analyze_emojis(messages)
    # Expected frequencies based on the mock data above
    expected = {
        "🎉": 3,
        "🍕": 2,
        "☀️": 1,
        "😢": 1,
    }
    assert result == expected

def test_cli_output(tmp_path, capsys):
    # Create a temporary messages file
    content = "Happy day 😊\nSad day 😢\nHappy again 😊"
    file_path = tmp_path / "messages.txt"
    file_path.write_text(content, encoding="utf-8")
    # Invoke the CLI entry point
    emoji_analyzer.main.__globals__["sys"].argv = ["emoji_analyzer", str(file_path)]
    emoji_analyzer.main()
    captured = capsys.readouterr().out
    # Parse JSON output
    output = json.loads(captured)
    assert output == {"😊": 2, "😢": 1}
