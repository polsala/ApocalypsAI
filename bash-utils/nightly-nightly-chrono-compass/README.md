# Nightly Chrono-Compass

## Summary
The `nightly-chrono-compass` is a whimsical-yet-useful bash utility designed to help you navigate your digital wasteland by pointing out recently modified files and highlighting time-sensitive notes within them. It acts as a 'temporal anomaly detector' for your filesystem, ensuring no critical task or recent change goes unnoticed.

## Usage
```bash
bash src/nightly-chrono-compass.sh [DIRECTORY] [DAYS_AGO] [KEYWORD1 KEYWORD2 ...]
```

### Arguments:
- `DIRECTORY`: (Optional) The path to the directory you want to scan. Defaults to the current directory (`.`).
- `DAYS_AGO`: (Optional) An integer specifying how many days back to look for recently modified files. Files modified within this many days (inclusive) will be considered 'recent'. Defaults to `1` (meaning files modified today or yesterday).
- `KEYWORD1 KEYWORD2 ...`: (Optional) One or more keywords to search for within the content of the recent files. The search is case-insensitive. If no keywords are provided, the utility will only list recent files.

### Examples:
1.  **Scan current directory for files modified in the last day, no keywords:**
    ```bash
    bash src/nightly-chrono-compass.sh
    ```

2.  **Scan `/var/log` for files modified in the last 7 days:**
    ```bash
    bash src/nightly-chrono-compass.sh /var/log 7
    ```

3.  **Scan `~/projects` for files modified in the last 3 days, looking for 'TODO' or 'URGENT':**
    ```bash
    bash src/nightly-chrono-compass.sh ~/projects 3 TODO URGENT
    ```

## Output
The utility will print a "Temporal Anomaly Report" listing recent files. For each recent file, if keywords were provided, it will also list the lines where those keywords were found, prefixed with "Whispers of urgency:". If no keywords are found in a recent file, it will indicate "No specific whispers detected within this echo."

Stay vigilant, wanderer!
