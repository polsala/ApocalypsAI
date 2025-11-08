# Survival Skill Suggester

A whimsical-yet-useful command-line utility designed to help you prepare for the inevitable (or just a bad camping trip). Provide a keyword or scenario, and the ApocalypsAI will suggest a crucial survival skill to master, complete with a description and a dose of dark humor.

## Purpose

In an ever-unpredictable world, being prepared is key. This utility aims to:
- **Educate**: Introduce users to fundamental survival skills.
- **Entertain**: Deliver advice with a unique, ApocalypsAI-flavored twist.
- **Empower**: Encourage learning practical skills that could genuinely be useful.

## How to Use

### Prerequisites

- Python 3.x

### Running the Suggester

Navigate to the `utils/survival-skill-suggester/` directory.

To get a general suggestion:
```bash
python src/suggester.py
```

To get a suggestion based on a keyword (e.g., "water", "food", "shelter", "first aid", "navigation", "fire", "communication", "defense"):
```bash
python src/suggester.py water
```

You can use multiple words, and the utility will try to find the best match:
```bash
python src/suggester.py "I'm worried about finding clean water"
```

Example Output:
```
--- Your ApocalypsAI Survival Skill Suggestion ---
Skill: Water Purification & Sourcing
Description: Learn how to find, filter, and purify water from various sources. Essential for long-term survival.
Whimsical Wisdom: Remember, even irradiated puddles can be... less irradiated with the right technique!

Stay vigilant, future survivor!
```

## Development

### Project Structure

```
survival-skill-suggester/
├── README.md
├── src/
│   └── suggester.py    # The core utility logic
└── tests/
    └── test_suggester.py # Unit tests for the suggester
```

### Testing

To run the tests, navigate to the `utils/survival-skill-suggester/` directory and execute:

```bash
python -m unittest tests/test_suggester.py
```

All tests are designed to be deterministic and run offline, using mocks for any random selections to ensure consistent results.
