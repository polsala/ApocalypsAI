# Mock rationale: No external services are called; tests are fully deterministic.

import os
import sys

# Ensure the src directory is on the import path.
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from emoji_analyzer import analyze_mood


def test_positive_mood():
    text = "I love sunny days and wonderful friends!"
    assert analyze_mood(text) == "😊"


def test_negative_mood():
    text = "I hate rain and terrible traffic."
    assert analyze_mood(text) == "😞"


def test_neutral_mood():
    text = "The cat sits on the mat."
    assert analyze_mood(text) == "😐"
