# Cron Expression Describer

A lightweight, self‑contained Python utility that converts a classic 5‑field cron expression into a readable English sentence.

## Features
- Parses minute, hour, day‑of‑month, month, and weekday fields.
- Handles `*` (any) and single numeric values.
- Provides a concise description like:
  ```
  "At minute 30, every hour, on day 15 of every month, on weekdays Monday, Wednesday, Friday."
  ```
- No third‑party dependencies – pure standard library.
- Comes with deterministic unit tests that run offline.

## Usage
```bash
python -m utils.cron-expression-describer.src.describe "30 * 15 * 1,3,5"
```
Will output:
```
At minute 30, every hour, on day 15 of every month, on weekdays Monday, Wednesday, Friday.
```

## Running the tests
```bash
cd utils/cron-expression-describer
python -m unittest discover -s tests
```
