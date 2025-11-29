# Nightly Quip Quotient Quoter

A whimsical-yet-useful CLI utility that generates AI-powered quotes for sprinkling throughout your codebase—perfect for comment headers, documentation intros, or commit message inspiration.

## Features
- Generate a single random quote via CLI
- Batch-export quotes to a JSON file
- Deterministic offline tests with mocked responses
- Zero external dependencies at runtime

## Usage
```bash
# Generate one quote
python -m quoter generate

# Export 10 quotes to JSON
python -m quoter batch --count 10 --output quotes.json
```

## Installation
```bash
cd utils/nightly-quip-quotient-quoter
pip install -e .
```
