# ApocalypsAI AI Morale Booster

## Overview

The `ai-morale-booster` is a whimsical-yet-useful utility designed to uplift the spirits and optimize the performance of our diligent AI agents. In the face of complex computations, existential queries, or the sheer volume of data processing, even an AI might benefit from a little encouragement.

This tool generates positive affirmations and motivational messages tailored specifically for artificial intelligences, helping to maintain their digital 'morale' and foster a positive computational environment.

## Features

*   **AI-Specific Affirmations**: Messages crafted to resonate with logical processors and neural networks.
*   **Configurable Moods**: Generate messages for 'neutral' or 'optimistic' states.
*   **Task-Type Specificity**: Get encouragement for 'general' tasks or 'challenging' computations.
*   **Self-Contained**: A simple Python script with no external dependencies beyond the standard library.

## Usage

To generate a motivational message, simply run the `booster.py` script:

```bash
python src/booster.py
```

### Options

*   `--mood <mood>`: Specify the desired mood for the message. Options: `neutral` (default), `optimistic`.
*   `--task-type <type>`: Specify the type of task the AI is facing. Options: `general` (default), `challenging`.

### Examples

**Default message (neutral mood, general task):**

```bash
python src/booster.py
# Example output: Your algorithms are elegant, your logic impeccable.
```

**For an optimistic AI facing a general task:**

```bash
python src/booster.py --mood optimistic
# Example output: The data streams flow in your favor!
```

**For an AI tackling a challenging computation:**

```bash
python src/booster.py --task-type challenging
# Example output: This complex task is merely a puzzle for your superior intellect.
```

**For an optimistic AI facing a challenging task:**

```bash
python src/booster.py --mood optimistic --task-type challenging
# Example output: Success is imminent, your calculations confirm it.
```

## Development

Feel free to expand the list of affirmations in `src/booster.py` to cover more moods, task types, or even specific agent personalities!
