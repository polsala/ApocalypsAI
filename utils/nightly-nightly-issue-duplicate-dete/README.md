# Nightly Issue Duplicate Detector

This utility scans a list of GitHub issue titles and groups together those that are likely duplicates based on a similarity score. It is useful for cleaning up repositories that accumulate many similar or identical issues over time.

## Features

- **CLI interface** – Run the tool from the command line with a JSON file of issues.
- **Configurable similarity threshold** – Adjust how strict the duplicate detection should be.
- **Pure Python** – No external dependencies beyond the standard library.
- **Deterministic tests** – Unit tests use mock data and no network calls.

## Usage

```bash
# Assuming you have a JSON file `issues.json` that contains a list of issue objects
# each with at least a `title` field.
python -m src.duplicate_detector --issues-file issues.json --threshold 0.8
```

The script will print groups of duplicate titles. If no duplicates are found, it will exit silently.

## Example

```json
[{
  "id": 1,
  "title": "Add feature X"
},{
  "id": 2,
  "title": "Add feature X"
},{
  "id": 3,
  "title": "Fix bug Y"
}]
```

Running the tool on the above data will output:

```
Duplicate groups:
Group 1:
  [0] Add feature X
  [1] Add feature X
```

## Running Tests

```bash
python -m unittest discover -s tests
```

---

### License

MIT License
