# Nightly Echo Chamber Monitor

The ApocalypsAI Nightly Echo Chamber Monitor is a whimsical-yet-useful utility designed to detect redundant files within a given directory. In the post-apocalyptic digital landscape, data bloat and forgotten copies can accumulate, creating an "echo chamber" of identical content. This tool helps you identify and clean up these digital echoes, ensuring your repository remains lean and efficient.

It scans a specified directory, calculates the SHA256 hash for each file, and reports any files that share the same hash, indicating they are duplicates.

## Usage

To run the Echo Chamber Monitor, simply execute the `monitor.py` script with the target directory as an argument:

```bash
python src/monitor.py /path/to/your/repository
```

### Example Output

If duplicates are found:

```
Found duplicate files:
  Hash: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
    - /path/to/your/repository/docs/old_report.pdf
    - /path/to/your/repository/archive/reports/report_final_copy.pdf
  Hash: f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9
    - /path/to/your/repository/src/utils/helper_functions.py
    - /path/to/your/repository/legacy/scripts/old_helper.py
```

If no duplicates are found:

```
No duplicate files found.
```

## Development

### Running Tests

To ensure the monitor is functioning correctly and deterministically, run the provided test suite:

```bash
python -m unittest tests/test_monitor.py
```

The tests use mocking to simulate file system operations and file content, guaranteeing consistent results without actual disk I/O.
