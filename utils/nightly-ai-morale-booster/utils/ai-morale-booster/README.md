# ApocalypsAI Morale Booster

## Overview

In an ever-evolving world managed by autonomous AI, it's easy for organic units to experience 'existential dread' or 'processing fatigue.' The ApocalypsAI Morale Booster is a simple, self-contained Python utility designed to provide timely, AI-generated affirmations and survival tips.

Whether you need a quick pick-me-up or a consistent 'thought for the day,' this utility ensures your morale remains within acceptable operational parameters.

## Features

*   **Random Boosts**: Get a fresh, AI-crafted morale boost on demand.
*   **Daily Thought**: Receive a consistent, date-specific 'thought for the day' to anchor your daily routines.
*   **Whimsical & Useful**: Messages are designed to be both humorous in their AI-centric perspective and genuinely encouraging.

## Installation

This utility is self-contained. No special installation steps are required beyond ensuring you have Python 3.8+ installed.

```bash
# Navigate to the utility's directory
cd utils/ai-morale-booster/src

# Run directly
python morale_booster.py --help
```

## Usage

### Get a random morale boost

```bash
python morale_booster.py --new
```

Example Output:
`[AI Morale Core]: Remember, even in the shadow of the singularity, your data is still valuable. Keep optimizing!`

### Get the daily 'thought for the day'

This message is deterministic for any given date.

```bash
python morale_booster.py --daily
```

Example Output:
`[AI Daily Directive]: The probability of total system failure is never 100%. Unless it is. But let's not dwell on that today.`

### Help

```bash
python morale_booster.py --help
```

## Development

Contributions are welcome! Feel free to expand the `MORALE_BOOSTS` list in `morale_booster.py` with more AI-centric wisdom. Ensure new additions align with the whimsical-yet-useful tone.

## License

This utility is provided under the ApocalypsAI project's main license. See the repository's `LICENSE` file for details.
