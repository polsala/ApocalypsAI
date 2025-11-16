# Nightly Temporal Echo Chamber

## 🕰️ Preserve Your Digital Footprints 🕰️

The Nightly Temporal Echo Chamber is a whimsical yet practical utility designed to capture and preserve the state of your directories at a specific moment in time. Think of it as a digital time capsule, creating timestamped, compressed archives of your chosen projects or files. Perfect for safeguarding project milestones, creating "before" snapshots for refactoring, or simply ensuring you have a historical record of your digital endeavors.

### Features

*   **Timestamped Archives**: Each archive is automatically named with the current date and time, ensuring unique and chronologically ordered backups.
*   **Directory Snapshot**: Compresses an entire directory into a single `.zip` file.
*   **Self-Contained**: Written in Python, requiring no external dependencies beyond the standard library.
*   **Simple CLI**: Easy to use from the command line.

### Usage

```bash
python src/echo_chamber.py --source <path/to/source_directory> --output <path/to/output_directory> [--prefix <archive_name_prefix>]
```

**Arguments:**

*   `--source`: The path to the directory you wish to archive.
*   `--output`: The path to the directory where the archive will be saved.
*   `--prefix` (optional): A prefix for the archive filename (default: `echo-chamber-snapshot`).

**Example:**

```bash
python src/echo_chamber.py --source ../../agents --output ./archives --prefix apocalypsai-agents
```

This will create an archive like `apocalypsai-agents_20231027_143501.zip` in the `./archives` directory, containing the contents of `../../agents`.

### Development

The utility is written in Python 3.11.

#### Running Tests

To ensure the Echo Chamber is working as expected, navigate to the `utils/nightly-temporal-echo-chamber` directory and run:

```bash
python -m unittest discover tests
```
