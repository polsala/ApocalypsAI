# Survival Skill Scrambler

## Overview

The `survival-skill-scrambler` is a whimsical utility designed to inject a bit of preparedness fun into your daily routine. Each time it runs, it presents you with a random, practical survival skill challenge or task. From identifying edible plants to practicing essential knots, this tool helps you gradually build a repertoire of skills that might just come in handy when the unexpected happens – or simply provides a fun learning prompt.

## Usage

To get your daily survival challenge, navigate to the utility's directory and run the `scrambler.py` script:

```bash
cd utils/survival-skill-scrambler
python src/scrambler.py
```

The script will output a single survival challenge to your console.

## Examples

```
$ python src/scrambler.py
Your survival challenge for today: Learn to identify 3 edible wild plants in your local area (and 1 poisonous one!).

$ python src/scrambler.py
Your survival challenge for today: Practice tying 5 essential knots: bowline, clove hitch, square knot, sheet bend, taut-line hitch.
```

## Development

### Skills List

The list of survival skills is defined within `src/scrambler.py`. You can easily extend or modify this list to include new challenges.

### Testing

Tests are located in `tests/test_scrambler.py` and ensure the utility functions as expected. To run tests, navigate to the utility's directory and execute:

```bash
cd utils/survival-skill-scrambler
python -m unittest tests/test_scrambler.py
```
