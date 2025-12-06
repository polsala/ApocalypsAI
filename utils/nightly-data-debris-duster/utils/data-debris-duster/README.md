# Data Debris Duster

## 🧹 Dusting Off Digital Debris

In the desolate digital wasteland, unused and empty directories accumulate like radioactive dust. The Data Debris Duster is a whimsical-yet-useful utility designed to help you identify and clean up these forgotten corners of your filesystem, ensuring your data bunkers remain tidy and efficient.

It's not just cleanup; it's digital archaeology!

## ✨ Features

*   **Scan**: Recursively identifies all empty directories within a specified path.
*   **Report**: Provides a clear list of detected "debris piles."
*   **Clean**: Optionally removes the identified empty directories.
*   **Safe**: Only targets truly empty directories.

## 🚀 Usage

```bash
python src/duster.py <path_to_scan> [--clean]
```

### Examples:

Scan your current directory for empty folders:
```bash
python src/duster.py .
```

Scan your 'downloads' folder and remove any empty directories found:
```bash
python src/duster.py ~/Downloads --clean
```

## 🛠️ Development

### Running Tests

To ensure the Duster is always ready for action, run its self-contained tests:

```bash
python -m unittest tests/test_duster.py
```
