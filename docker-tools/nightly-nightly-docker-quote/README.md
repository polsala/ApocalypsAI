Nightly Docker Quote
====================

This utility builds a Docker image that prints a random quote from a bundled list each time it runs.

Usage
-----

```bash
docker build -t nightly-quote .
docker run --rm nightly-quote
```

The container will output a single quote and exit.

The quotes are stored in `src/quotes.txt`. You can add or edit quotes as you wish.

Testing
-------

Run the tests with:

```bash
python -m unittest discover -s tests
```
