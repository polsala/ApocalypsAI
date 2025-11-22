# Nightly Env-Var Enforcer

The Nightly Env-Var Enforcer is a whimsical-yet-crucial utility designed to ensure your operational environment is perfectly aligned with expectations. Like a diligent digital guardian, it scans for specified environment variables, verifying their presence and ensuring they aren't merely empty shells. This helps prevent unexpected runtime errors and ensures your applications launch with all the necessary cosmic energies.

## Purpose

Many applications rely on environment variables for configuration, API keys, database connections, and more. A missing or empty environment variable can lead to cryptic errors or silent failures. This utility provides a quick, automated check to validate your environment before critical processes begin.

## Usage

Run the `enforcer.py` script with a comma-separated list of environment variable names you wish to enforce.

```bash
python src/enforcer.py VAR_NAME_1,VAR_NAME_2,ANOTHER_IMPORTANT_VAR
```

### Example

Let's say you need `API_KEY`, `DB_HOST`, and `DEBUG_MODE` to be set.

```bash
# Scenario 1: All variables are present and non-empty
export API_KEY="supersecret"
export DB_HOST="localhost"
export DEBUG_MODE="true"
python src/enforcer.py API_KEY,DB_HOST,DEBUG_MODE

# Expected Output:
# --- Nightly Env-Var Enforcement Report ---
# ✅ PRESENT: Environment variable 'API_KEY' is set and non-empty.
# ✅ PRESENT: Environment variable 'DB_HOST' is set and non-empty.
# ✅ PRESENT: Environment variable 'DEBUG_MODE' is set and non-empty.
# ------------------------------------------
# All required environment variables are present and non-empty. Good to go!
```

```bash
# Scenario 2: Some variables are missing or empty
export API_KEY="supersecret"
# DB_HOST is missing
export DEBUG_MODE="" # DEBUG_MODE is empty
python src/enforcer.py API_KEY,DB_HOST,DEBUG_MODE

# Expected Output:
# --- Nightly Env-Var Enforcement Report ---
# ✅ PRESENT: Environment variable 'API_KEY' is set and non-empty.
# ❌ MISSING: Environment variable 'DB_HOST' is not set.
# ⚠️ EMPTY: Environment variable 'DEBUG_MODE' is set but empty.
# ------------------------------------------
# Some required environment variables are missing or empty. Please address them.
```

## Development & Testing

The utility is written in Python 3.11 and uses standard library features.

To run tests:

```bash
python -m unittest tests/test_enforcer.py
```

Tests use `unittest.mock` to simulate `os.environ` and `sys.argv` for deterministic and offline execution.
