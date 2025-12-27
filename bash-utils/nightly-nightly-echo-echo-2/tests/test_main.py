import subprocess
import os
import re

# Helper to run the script with optional environment overrides

def run_script(env=None):
    env_vars = os.environ.copy()
    if env:
        env_vars.update(env)
    result = subprocess.run(
        ["bash", "src/main.sh"],
        capture_output=True,
        text=True,
        env=env_vars,
    )
    return result.stdout.strip()

# Test that the timestamp is in ISO 8601 UTC format

def test_timestamp_format():
    output = run_script()
    match = re.match(r"\[(.*?)\] (.*)", output)
    assert match, f"Output did not match expected pattern: {output}"
    timestamp = match.group(1)
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp), f"Timestamp format incorrect: {timestamp}"

# Test that the phrase is one of the predefined list when no override is set

def test_random_phrase():
    output = run_script()
    match = re.match(r"\[(.*?)\] (.*)", output)
    assert match, f"Output did not match expected pattern: {output}"
    phrase = match.group(2)
    allowed = [
        "Keep calm and carry on.",
        "The only limit is your mind.",
        "Every day is a new adventure.",
        "Believe you can and you're halfway there.",
        "Stay curious, stay humble.",
    ]
    assert phrase in allowed, f"Phrase not in allowed list: {phrase}"

# Test that overriding the phrase works deterministically

def test_override_phrase():
    custom = "Test phrase"
    output = run_script({"ECHO_ECHO_PHRASE": custom})
    match = re.match(r"\[(.*?)\] (.*)", output)
    assert match, f"Output did not match expected pattern: {output}"
    phrase = match.group(2)
    assert phrase == custom, f"Expected overridden phrase '{custom}', got '{phrase}'"
