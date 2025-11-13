import sys
import os
import importlib

# Mock rationale: Ensure deterministic output by patching random.choice
# Adjust sys.path to import the utility's src module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import main

def test_get_random_quote(monkeypatch):
    # Patch random.choice to always return the first quote
    monkeypatch.setattr(main.random, "choice", lambda seq: seq[0])
    quote = main.get_random_quote()
    assert quote == "Believe you can and you're halfway there."

def test_cli_output(monkeypatch, capsys):
    # Patch random.choice to return the second quote
    monkeypatch.setattr(main.random, "choice", lambda seq: seq[1])
    main.main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "The only way to do great work is to love what you do."
