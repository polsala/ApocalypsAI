# Nightly Daily Quip Generator

**What it does**

- Generates a short, witty programming‑related quip that changes every day.
- The quip is *deterministic*: the same calendar date always yields the same quote, so the output is reproducible and testable.
- Implemented in pure Python 3.11 with only the standard library.

**How to use**

```bash
# Run the utility (prints today’s quip)
python -m utils.nightly-daily-quip-generator.src.quip_generator
```

Or import it in your own code:

```python
from utils.nightly-daily-quip-generator.src.quip_generator import get_daily_quip

print(get_daily_quip())          # today’s quip
print(get_daily_quip(date(2023, 1, 1)))  # quip for a specific date
```

**Running the tests**

```bash
python -m unittest discover -s utils/nightly-daily-quip-generator/tests
```

**Design notes**

- The quip is selected by taking the date’s ordinal (`date.toordinal()`) modulo the number of available quotes. This avoids any randomness or external services.
- The utility is deliberately lightweight so it can run in any CI environment without additional dependencies.
