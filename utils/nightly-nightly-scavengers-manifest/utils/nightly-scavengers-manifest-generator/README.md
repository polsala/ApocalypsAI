# Nightly Scavenger's Manifest Generator

## Description
In the post-apocalyptic digital wasteland, data can be as valuable as clean water. The `Nightly Scavenger's Manifest Generator` is a crucial utility for cataloging your digital findings. It scans a specified directory, identifies all files, categorizes them by their extensions, and compiles a comprehensive manifest. This manifest provides a quick overview of your data hoard, including file counts, total sizes, and the last time you 'scavenged' (modified) them.

## Usage
Run the `manifest_generator.py` script with the target directory as an argument.

```bash
python src/manifest_generator.py /path/to/your/data/hoard
```

To save the manifest to a file:

```bash
python src/manifest_generator.py /path/to/your/data/hoard --output manifest.txt
```

## Example Output
```
Scavenger's Manifest for: /path/to/your/data/hoard
Generated On: 2023-10-27 10:30:00

Total Files Scanned: 10
Total Size: 12.5 MB

--- File Type Summary ---
.txt:
  Count: 3
  Total Size: 2.1 MB
  Last Modified (oldest): 2023-01-15 08:00:00
  Last Modified (newest): 2023-09-20 14:15:00

.log:
  Count: 5
  Total Size: 8.9 MB
  Last Modified (oldest): 2022-11-01 06:00:00
  Last Modified (newest): 2023-10-26 23:59:59

.json:
  Count: 2
  Total Size: 1.5 MB
  Last Modified (oldest): 2023-03-10 11:00:00
  Last Modified (newest): 2023-07-01 16:00:00

--- End Manifest ---
```
