# Nightly Quote Keeper

**What it does**

`nightly-quote-keeper` is a tiny, self‑contained utility that prints a random inspirational quote to the console.  You can optionally filter quotes by a tag (e.g., `motivation`, `humor`).  The entire quote database lives inside the package – no network access required.

**Why it’s useful**

- Add a daily dose of motivation to CI logs, terminal sessions, or scripts.
- No external dependencies beyond the Python standard library.
- Fully tested and deterministic – perfect for the ApocalypsAI “nightly” philosophy.

**Installation**

The utility lives under `utils/nightly-quote-keeper`.  To use it, simply add the repository to your `PYTHONPATH` or run it via the module syntax:

```bash
python -m utils.nightly-quote-keeper.src.quote_keeper
```

You can also import the library in your own code:

```python
from utils.nightly-quote-keeper.src.quote_keeper import get_random_quote

print(get_random_quote())
```

**CLI usage**

```bash
# Print any random quote
python -m utils.nightly-quote-keeper.src.quote_keeper

# Filter by tag (case‑insensitive)
python -m utils.nightly-quote-keeper.src.quote_keeper --tag motivation
```

**Running the tests**

```bash
cd utils/nightly-quote-keeper
python -m unittest discover -s tests
```

**Design notes**

- Quotes are stored as a frozen `@dataclass` list inside the module – no external files.
- Randomness is isolated to `random.choice`; the test suite patches this to guarantee deterministic outcomes.
- Errors for unknown tags are reported via `argparse` so the CLI behaves like standard Unix tools.
