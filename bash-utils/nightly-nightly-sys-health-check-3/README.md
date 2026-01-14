# nightly-sys-health-check

A whimsical yet useful bash script to perform a quick system health check. It reports on disk space, memory usage, and running processes, all with a touch of apocalyptic flair.

## Usage

Run the script from your terminal:

```bash
./src/main.sh
```

## Output

The script will output a series of status messages, indicating the health of your system. Expect messages like:

*   `Disk space: Sufficient for the last stand!`
*   `Memory usage: Plenty of RAM for your escape pod!`
*   `Running processes: All systems nominal, no immediate threats detected.`

Or, if things are looking grim:

*   `Disk space: WARNING! Running low on space for bunkers!`
*   `Memory usage: CRITICAL! Your system is struggling to keep up with the apocalypse!`
*   `Running processes: ALERT! Unidentified processes detected, potential saboteurs!`

## Tests

Automated tests are included to ensure the script functions as expected. Run them using `bash`:

```bash
./tests/test_main.sh
```
