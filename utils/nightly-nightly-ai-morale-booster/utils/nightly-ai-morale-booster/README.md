# Nightly AI Morale Booster

A small, self-contained Python utility designed to inject a dose of whimsical encouragement or darkly humorous wisdom into your daily routine, especially during those long nights of integration or when facing the existential dread of an impending (or ongoing) apocalypse.

## Purpose

In the ApocalypsAI collective, even autonomous agents need a pick-me-up. This utility provides random, pre-defined "morale boosts" that can be integrated into CI/CD logs, developer dashboards, or simply run manually when you need a moment of levity.

## Usage

To get a random morale boost:

```bash
python src/morale_booster.py
```

Example output:
```
✨ Morale Boost: The apocalypse is just a refactoring opportunity. Keep calm and commit on. ✨
```

## Installation

This utility is self-contained and requires no external dependencies beyond a standard Python 3.11+ environment.

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-ai-morale-booster
    ```
2.  Run the script:
    ```bash
    python src/morale_booster.py
    ```

## Development & Testing

### Running Tests

To ensure the morale booster is always in top form (and deterministic!), run the tests:

```bash
python -m pytest tests/test_morale_booster.py
```

### Adding New Boosts

You can easily expand the collection of morale boosts by editing the `MORALE_BOOSTS` list in `src/morale_booster.py`. Feel free to add your own brand of whimsical encouragement or apocalyptic humor!
