# Nightly Temporal Tear Tracker

## Unearthing Digital Relics from Forgotten Eras

The ApocalypsAI Nightly Integrator presents the Temporal Tear Tracker, a crucial utility for maintaining a lean and relevant digital landscape in the post-apocalyptic world. This tool scans a specified directory for files that haven't been modified in a configurable number of days, identifying them as "temporal tears" – forgotten relics of a bygone era that might be ripe for archival, deletion, or re-evaluation.

Keep your data fresh and your storage optimized by regularly tracking these digital echoes!

## Usage

```bash
python src/tracker.py --path <directory_to_scan> --age <days_since_last_modification>
```

### Arguments:
*   `--path <directory_to_scan>`: The root directory to start scanning from. The utility will recursively check all subdirectories.
*   `--age <days_since_last_modification>`: The minimum number of days a file must not have been modified to be considered a "temporal tear."

## Example

To find all files in your current directory that haven't been modified in the last 90 days:

```bash
python src/tracker.py --path . --age 90
```

Output will be a list of file paths and their last modification dates:

```
Temporal Tears (files not modified in 90 days):
/path/to/your/project/old_script.py (Last Modified: 2023-01-15 10:30:00)
/path/to/your/project/docs/ancient_plan.md (Last Modified: 2022-11-01 14:00:00)
```
