#!/bin/bash
set -euo pipefail

echo "Running Nightly Mood Beacon unit tests..."

# Create a temporary virtual environment
python -m venv .venv_test
source .venv_test/bin/activate

# Install dependencies for testing
pip install Flask pytest

# Run the tests
pytest tests/test_app.py

# Deactivate virtual environment and clean up
deactivate
rm -rf .venv_test

echo "Nightly Mood Beacon tests completed."
