# Nightly Gloom-Glimmer Greeter

## Overview

The `nightly-gloom-glimmer-greeter` is a small, self-contained command-line utility designed to offer a moment of whimsical encouragement or darkly humorous wisdom to the weary survivor. Each time it's run, it presents a random greeting and a practical (or comically impractical) survival tip, perfect for starting your day in the post-apocalyptic landscape with a smile or a grim chuckle.

## Usage

To run the greeter, navigate to the `src` directory and execute the Python script:

```bash
python src/greeter.py
```

### Example Output

```
Greetings, survivor! Another cycle dawns.
Survival Tip: Always check your boots for scorpions before putting them on. Trust us on this one.
```

## Development

This utility is written in Python 3.x and has no external dependencies beyond the standard library.

### Running Tests

To ensure the greeter is functioning as expected, run the tests from the utility's root directory:

```bash
python -m unittest tests/test_greeter.py
```
