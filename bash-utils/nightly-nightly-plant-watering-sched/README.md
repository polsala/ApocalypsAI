Nightly Plant Watering Scheduler
================================

Overview
--------
This tiny bash utility helps you keep your houseplants alive in the post‑apocalyptic world. It stores the last‑watered date for each plant and, when run, tells you which plants are overdue for a drink.

Features
--------
* Simple line‑based storage (plant:YYYY‑MM‑DD) – no external databases.
* Configurable watering interval (default: 7 days).
* Ability to record a watering event via `--water <plant>`.
* Fully offline – works on any POSIX‑compatible shell.

Installation
------------
1. Copy the `src/main.sh` script to a location in your `$PATH` (e.g., `~/bin/plant-watering`).
2. Make it executable: `chmod +x ~/bin/plant-watering`.

Configuration (environment variables)
------------------------------------
* `PLANT_DATA_FILE` – Path to the data file. Defaults to `$HOME/.plant_watering`.
* `INTERVAL_DAYS` – Number of days after which a plant is considered thirsty. Default is `7`.
* `CURRENT_DATE` – Override the current date (format `YYYY-MM-DD`). Useful for testing. If unset, the script uses `date +%Y-%m-%d`.

Usage
-----
* List plants that need water:
  ```
  plant-watering
  ```
* Record that you just watered a plant:
  ```
  plant-watering --water <plant-name>
  ```
  Example: `plant-watering --water cactus`

The script will output a friendly message confirming the record.

Testing
-------
Run the bundled test suite with:
```bash
cd tests && ./test_main.sh
```
All tests should pass on any Unix‑like system.

License
-------
Public domain – feel free to adapt, remix, and share.
