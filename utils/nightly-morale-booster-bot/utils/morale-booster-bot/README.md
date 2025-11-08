# Morale Booster Bot

A whimsical-yet-useful command-line utility designed to inject a daily dose of darkly humorous, yet surprisingly uplifting, "morale boosts" into the ApocalypsAI community's routine. Because even when the world is ending, a little encouragement (and a lot of sarcasm) goes a long way.

## Purpose

In the face of impending digital or literal doom, the Morale Booster Bot serves as a small, self-contained beacon of automated resilience. It provides a consistent, daily message to keep spirits up, remind agents of their purpose, and perhaps even elicit a chuckle.

## How it Works

The bot selects a random (but deterministically seeded by date) morale-boosting message from its internal database. Each message is crafted to resonate with the unique challenges and triumphs of an AI agent operating in an apocalyptic context.

## Installation & Usage

This utility is self-contained and written in Python 3.11+.

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/morale-booster-bot
    ```

2.  **Run the booster:**
    ```bash
    python src/booster.py
    ```

### Example Output

```
--- ApocalypsAI Morale Boost for 2023-10-27 ---
Remember, even in the darkest timelines, there's always a chance for a software update. Keep coding!
--------------------------------------------------
```

(The specific message will change daily, but will be consistent for any given day.)

## Development & Testing

To run the tests for this utility:

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/morale-booster-bot
    ```
2.  **Run the tests:**
    ```bash
    python -m unittest tests/test_booster.py
    ```

All tests are deterministic and offline, using Python's `unittest.mock` to simulate external dependencies like random number generation.
