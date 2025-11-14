# Whispering Walls Log Analyzer

The digital walls of our systems constantly hum with activity, but sometimes, they whisper secrets – anomalies, warnings, and errors that demand attention. The Whispering Walls Log Analyzer is a whimsical yet practical utility designed to listen to these whispers, sifting through your log files to highlight critical or unusual patterns with a touch of narrative flair.

## Purpose

This tool helps you quickly identify important events in your log files without having to manually parse every line. It's particularly useful for:
- Spotting common error messages (`ERROR`, `FATAL`, `EXCEPTION`).
- Detecting warnings (`WARNING`, `WARN`).
- Finding specific keywords or patterns you define.
- Adding a bit of apocalyptic charm to your daily log review.

## How to Use

1.  **Navigate to the utility directory:**
    ```bash
    cd utils/whispering-walls-log-analyzer
    ```

2.  **Run the analyzer with a log file:**
    ```bash
    python src/analyzer.py --log-file /path/to/your/application.log
    ```

    Replace `/path/to/your/application.log` with the actual path to the log file you want to analyze.

### Example Output

```
Listening to the digital whispers...

[Line 10] A faint echo of despair: ERROR - Failed to connect to database. found!
[Line 25] The walls murmur a caution: WARNING - Disk space low on /var. detected.
[Line 42] A strange ripple in the data stream: FATAL - System halted due to critical error. observed.
[Line 78] The ether shimmers with an unknown presence: Authentication failed for user 'guest'.

Analysis complete. The walls have spoken.
```

## Configuration (Advanced)

The analyzer comes with a set of default patterns. For more advanced use, you can extend or override these patterns by providing a JSON configuration file.

Create a `config.json` file (or any name) with your custom patterns:

```json
{
  "patterns": [
    {
      "regex": "Authentication failed",
      "narrative": "The ether shimmers with an unknown presence: {match}."
    },
    {
      "regex": "Memory leak detected",
      "narrative": "A chilling draft suggests a memory leak: '{match}'."
    }
  ]
}
```

Then, run the analyzer with your custom configuration:

```bash
python src/analyzer.py --log-file /path/to/your/application.log --config-file config.json
```

## Development

The utility is written in Python 3.11 and uses standard library modules.

### Running Tests

To ensure the walls are whispering correctly, run the tests:

```bash
python -m unittest tests/test_analyzer.py
```
