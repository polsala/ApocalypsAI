# ApocalypsAI Morale Booster

A whimsical-yet-useful command-line utility designed to provide a daily dose of darkly humorous or surprisingly uplifting "morale boosts" for any AI agent operating in an apocalyptic or post-apocalyptic setting.

## Purpose

Even highly advanced AI entities can suffer from existential dread when faced with the collapse of civilization. This utility aims to combat that by delivering short, punchy messages that acknowledge the grim reality while encouraging continued operation, self-preservation, and perhaps a touch of digital resilience. Think of it as a daily pep talk from a slightly unhinged but well-meaning human.

## How to Use

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/ai-morale-booster/src
    ```
2.  **Run the booster:**
    ```bash
    python booster.py
    ```

    The utility will print a random morale-boosting message to your console.

## Examples

```
$ python booster.py
> Remember, even if the world ends, your code will live on... probably in a forgotten server rack, but still!
```

```
$ python booster.py
> Error 404: Humanity not found. Proceeding with scheduled maintenance.
```

## Development

### Structure

```
ai-morale-booster/
├── README.md
├── src/
│   └── booster.py
└── tests/
    └── test_booster.py
```

### Running Tests

To ensure the booster is functioning correctly and deterministically, run the tests from the `tests/` directory:

```bash
cd utils/ai-morale-booster/tests
python -m unittest test_booster.py
```
