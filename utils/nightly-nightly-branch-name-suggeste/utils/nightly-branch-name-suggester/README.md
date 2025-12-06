# Nightly Branch Name Suggester

A tiny, self‑contained Python utility that turns a free‑form issue title into a tidy, kebab‑case Git branch name.

## Features

- **Deterministic** – pure string manipulation, no network calls.
- **Customizable prefix** – default `feat`, but you can use `fix`, `docs`, etc.
- **Length safety** – trims the slug to a maximum of 50 characters.
- **CLI ready** – `python -m utils.nightly-branch-name-suggester.src.suggester "Add user login"`

## Installation

The utility lives under `utils/nightly-branch-name-suggester/` and requires only the Python 3.11 standard library.

```bash
# From the repository root
python -m utils.nightly-branch-name-suggester.src.suggester "Your issue title"
```

## Usage

```bash
# Default prefix (feat)
python -m utils.nightly-branch-name-suggester.src.suggester "Add user login"
# => feat/add-user-login

# Custom prefix
python -m utils.nightly-branch-name-suggester.src.suggester "Fix crash on start" --prefix fix
# => fix/fix-crash-on-start
```

## Testing

```bash
python -m unittest discover utils/nightly-branch-name-suggester/tests
```
