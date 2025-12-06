# Haiku Generator

**nightly‑haiku‑generator** creates a simple 5‑7‑5 haiku by randomly selecting lines from curated word lists. The generator is completely offline, has no external dependencies, and can be seeded for deterministic output – perfect for both playful moments and automated testing.

## Usage
```bash
# Run the generator (random output)
python -m src.haiku_generator

# Run with a seed for reproducible output
python -m src.haiku_generator --seed 42
```

## Example Output
```
Silent autumn leaves
The river sings a soft lullaby
Moonlight kisses earth
```

## How It Works
- Three small lists contain pre‑written lines that already satisfy the 5‑7‑5 syllable pattern.
- `generate_haiku(seed=None)` picks one line from each list using a `random.Random` instance.
- Supplying a seed makes the selection deterministic, which the test suite relies on.

## Testing
Run the tests with:
```bash
python -m unittest discover -s tests
```
All tests are offline and use `unittest.mock` to guarantee deterministic behaviour.
