# Nightly Forgotten Feature Finder

The `nightly-forgotten-feature-finder` is a whimsical-yet-useful utility designed to unearth those long-lost `TODO`, `FIXME`, `HACK`, and other technical debt markers lurking within your codebase. Like a digital archaeologist, it meticulously scans your project files to bring forgotten tasks and potential issues back into the light, ensuring no digital dust bunny goes unnoticed.

## Usage

To run the finder, navigate to your project's root directory and execute the `finder.py` script.

```bash
python src/finder.py [path_to_scan]
```

If `path_to_scan` is omitted, it defaults to the current directory (`.`).

### Example Output

```
Forgotten Features Report:

./src/main.py:10: TODO: Implement the advanced AI module.
./src/utils.py:25: FIXME: This function has a known race condition.
./docs/README.md:50: HACK: Temporary workaround for API rate limits.
./tests/test_feature.py:120: BUG: Test fails intermittently on CI.
```

## Configuration

The utility currently scans for `TODO`, `FIXME`, `HACK`, `BUG`, and `XXX` markers. Future versions might allow custom marker configuration.

## Development

### Running Tests

To ensure the finder is always sharp, run its self-contained tests:

```bash
python -m unittest tests/test_finder.py
```
