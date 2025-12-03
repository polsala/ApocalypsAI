# Nightly Survival Skill Scrambler

## Overview

The `nightly-survival-skill-scrambler` is a lighthearted yet practical command-line utility designed to help you prepare for any eventuality. Each time you run it, it suggests a random survival skill or preparedness task, encouraging you to learn, practice, or review something new to bolster your resilience.

Whether you're facing a zombie outbreak, a meteor shower, or just a Tuesday, this tool ensures you're always one step closer to becoming a post-apocalyptic pro.

## Usage

To get your daily dose of survival wisdom, simply navigate to the utility's directory and run the script:

```bash
cd utils/nightly-survival-skill-scrambler
python src/scrambler.py
```

It will output a single, actionable task for you to ponder or practice.

## Example Output

```
Your survival task for today: Practice knot-tying (bowline, square knot, sheet bend).
```

## Development

### Adding New Skills

To expand the repertoire of survival tasks, simply edit the `SKILLS` list within `src/scrambler.py`.

### Running Tests

Ensure the scrambler is functioning as expected by running its tests from the utility's root directory:

```bash
cd utils/nightly-survival-skill-scrambler
python -m unittest tests/test_scrambler.py
```
