# Nightly Chrono-Compass

## Summary
The `nightly-chrono-compass` is a whimsical-yet-useful bash utility designed to help you navigate your temporal landscape. It scans a specified directory for recently modified files, indicating "temporal disturbances," and highlights upcoming "temporal waypoints" (deadlines) defined in a simple configuration file.

This tool provides a quick overview of what demands your immediate attention, ensuring you stay on course in the ever-flowing river of time.

## Usage
To use the Chrono-Compass, simply run the script with a target directory and optional parameters:

```bash
src/chrono_compass.sh [OPTIONS] <directory>
```

### Arguments
* `<directory>`: The path to the directory you want the Chrono-Compass to scan for recent file modifications.

### Options
* `--waypoints <file>`: Specifies a text file containing your "temporal waypoints" (deadlines). Each line in this file should follow the format: `Task Name|YYYY-MM-DD`.
* `--lookback <days>`: The number of days to look back for recently modified files. Files modified within this period will be reported as "Recent Temporal Disturbances." Defaults to `1` (last 24 hours).
* `-h`, `--help`: Displays the usage information and exits.

## Temporal Waypoints File Format
The waypoints file should be a plain text file where each line represents a task and its deadline, separated by a pipe (`|`).

Example `my_deadlines.txt`:
```
Refactor Legacy Code|2023-10-29
Deploy New Feature|2023-10-31
Write Documentation|2023-11-04
Review PR #123|2023-10-27
```

## Examples

1. **Scan your current project directory for recent changes and upcoming deadlines:**
   ```bash
   src/chrono_compass.sh --waypoints my_deadlines.txt --lookback 3 ./my_project
   ```

2. **Check for files modified in the last 24 hours in your home directory (without waypoints):**
   ```bash
   src/chrono_compass.sh ~/my_documents
   ```

3. **Get help information:**
   ```bash
   src/chrono_compass.sh --help
   ```

## Output
The Chrono-Compass will output a report detailing:
* **Recent Temporal Disturbances**: Files modified within the specified lookback period, sorted by modification time.
* **Upcoming Temporal Waypoints**: Tasks from your waypoints file that are due today or in the future, with an indication of urgency (e.g., "TODAY!", "URGENT - 1 day left", "X days left").

```
🧭 Chrono-Compass Report 🧭

Scanning temporal currents in /path/to/project...

Recent Temporal Disturbances (Modified in last 1 day(s)):
  - /path/to/project/src/main.sh (Modified: 2023-10-27 10:30:00.123456789 +0000)
  - /path/to/project/README.md (Modified: 2023-10-27 09:15:00.987654321 +0000)

Upcoming Temporal Waypoints:
  - [TODAY!] Review PR #123 (Deadline: 2023-10-27)
  - [URGENT - 1 day left] Refactor Legacy Code (Deadline: 2023-10-28)
  - [4 days left] Deploy New Feature (Deadline: 2023-10-31)
  - Write Documentation (Deadline: 2023-11-04)

All clear on the temporal horizon for now. Keep an eye on the currents!
```
