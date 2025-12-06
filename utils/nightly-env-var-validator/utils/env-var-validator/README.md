# env-var-validator

A whimsical yet practical utility that validates the presence of required environment variables in a `.env` file.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- Accepts a comma‑separated list of required keys via CLI.
- Returns a clear, machine‑parseable JSON report of missing keys.
- Helpful exit codes:
  - `0` – all required keys are present.
  - `1` – one or more keys are missing.
  - `2` – usage error (e.g., file not found).

## Installation

Copy the `src/validator.py` file into your project or add the whole folder to your repository. No installation step is required.

## Usage

```bash
python -m env_var_validator \
    --env-file path/to/.env \
    --required KEY1,KEY2,KEY3
```

The tool prints a JSON object to `stdout`:

```json
{"missing": ["KEY2"]}
```

If all keys are present, the `missing` list is empty and the process exits with code `0`.

## Testing

Run the bundled tests with `pytest`:

```bash
pytest utils/env-var-validator/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
