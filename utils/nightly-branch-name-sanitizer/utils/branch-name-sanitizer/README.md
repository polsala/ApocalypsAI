# Branch Name Sanitizer

A tiny, self‑contained Python utility that converts arbitrary Git branch names into a safe, URL‑friendly format.

## Features

- Lower‑cases the name.
- Replaces spaces and underscores with hyphens.
- Strips characters that are not alphanumeric or hyphens.
- Collapses consecutive hyphens.
- Trims leading/trailing hyphens.

## Usage

```bash
python -m branch_name_sanitizer "Feature/Add New_Stuff!"
# => feature-add-new-stuff
```

You can also import the function in your own scripts:

```python
from src.sanitizer import sanitize_branch_name

clean = sanitize_branch_name("Feature/Add New_Stuff!")
print(clean)  # "feature-add-new-stuff"
```

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```

All tests are deterministic and run offline.
