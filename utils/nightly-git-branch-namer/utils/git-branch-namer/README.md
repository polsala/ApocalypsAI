# Git Branch Namer

A tiny, self‑contained Python utility that turns a human‑readable issue title into a clean, conventional git branch name.

## Features

* Simple **slugify**‑like conversion.
* Removes common stop‑words (`the`, `a`, `an`, `and`, `or`, `but`, `for`, `with`, `to`, `of`, `in`).
* Keeps only alphanumeric characters and hyphens.
* Truncates the result to a maximum of 50 characters to stay within typical git limits.
* Works offline – no external services required.

## Installation

Copy the `src/branch_namer.py` file into your project or add the whole folder to your repository.

## Usage

```bash
python -m src.branch_namer "Add user login feature with OAuth2"
# → add-user-login-feature-oauth2
```

You can also import the function in your own scripts:

```python
from src.branch_namer import suggest_branch_name

branch = suggest_branch_name("Fix bug in payment processing")
print(branch)  # → fix-bug-payment-processing
```

## Testing

Run the bundled unit tests with:

```bash
python -m unittest discover -s tests
```

## License

MIT
