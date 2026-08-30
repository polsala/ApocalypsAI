# Nightly Config Constellation Aligner

The digital cosmos can be a chaotic place, with environment variables drifting like rogue asteroids and config files diverging like distant galaxies. The **Nightly Config Constellation Aligner** is here to bring order to your universe!

This utility helps you harmonize your environment variables across multiple `.env` files (or similar key-value config files). It identifies:
*   **Missing Stars**: Variables present in some constellations but absent in others.
*   **Drifting Stars**: Variables present in all constellations but with differing values.
*   **Harmonized Stars**: Variables that are perfectly aligned across all your chosen constellations.

Bring celestial peace to your configurations!

## Installation

```bash
# Navigate to the utility directory
cd node-utils/nightly-config-constellator

# Install dependencies
npm install
```

## Usage

Run the utility with the paths to your configuration files. It supports `.env` files by default.

```bash
node src/index.js <path/to/env1> <path/to/env2> [path/to/env3 ...]
```

### Example

Let's say you have `dev.env` and `prod.env`:

**`dev.env`:**
```
API_KEY=dev_key
DEBUG_MODE=true
PORT=3000
FEATURE_FLAG=enabled
```

**`prod.env`:**
```
API_KEY=prod_key
PORT=8080
DATABASE_URL=postgres://user:pass@host:5432/db
```

Running `node src/index.js dev.env prod.env` would yield a report like:

```
🌌 Aligning Config Constellations 🌌

Comparing: dev.env, prod.env

--- Missing Stars ---
[dev.env] is missing:
  - DATABASE_URL
[prod.env] is missing:
  - DEBUG_MODE
  - FEATURE_FLAG

--- Drifting Stars ---
API_KEY:
  - dev.env: dev_key
  - prod.env: prod_key
PORT:
  - dev.env: 3000
  - prod.env: 8080

--- Harmonized Stars ---
  No perfectly aligned stars found.

✨ Constellations checked. May your configurations be ever aligned! ✨
```

## Development

### Running Tests

```bash
npm test
```
