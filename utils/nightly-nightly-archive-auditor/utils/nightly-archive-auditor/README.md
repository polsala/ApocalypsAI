# Nightly Archive Auditor

## 📜 Whimsical Purpose

In the post-apocalyptic digital wasteland, data accumulates like radioactive dust. The "Nightly Archive Auditor" is your trusty companion, sifting through the digital rubble to identify forgotten files – those relics of a bygone era that haven't been touched in ages. It helps you decide what to archive, what to delete, and what might just be a hidden treasure waiting to be rediscovered. Keep your digital bunker tidy!

## 🛠️ Utility

This utility scans a specified directory for files that have not been modified within a given timeframe (defaulting to one year). It then generates a clear Markdown report, listing these "stale" files, their last modification dates, and their age in days. This is invaluable for:

*   **Disk Space Management**: Identify large, forgotten files consuming precious storage.
*   **Data Hygiene**: Keep project directories clean and relevant.
*   **Compliance**: Pinpoint old logs or data that might need specific archiving policies.
*   **Digital Archaeology**: Sometimes, an old file is exactly what you need!

## 🚀 How to Use

### Prerequisites

*   Python 3.11 or higher

### Running the Auditor

1.  Navigate to the `utils/nightly-archive-auditor/` directory.
2.  Run the `auditor.py` script with the target directory and an optional age threshold:

    ```bash
    python src/auditor.py <path_to_directory_to_scan> [--age <number_of_days>]
    ```

    *   `<path_to_directory_to_scan>`: The absolute or relative path to the directory you want to audit.
    *   `--age <number_of_days>`: (Optional) The number of days after which a file is considered "stale". Defaults to `365` days (1 year).

### Examples

*   Scan your current working directory for files older than 1 year:
    ```bash
    python src/auditor.py .
    ```

*   Scan your `/home/user/documents` directory for files older than 90 days:
    ```bash
    python src/auditor.py /home/user/documents --age 90
    ```

*   Scan a project folder for files older than 2 years (730 days):
    ```bash
    python src/auditor.py ~/my_old_project --age 730
    ```

The report will be printed directly to your console (stdout). You can redirect it to a file if you wish:

```bash
python src/auditor.py . > archive_report.md
```

## 🧪 Testing

To ensure the auditor is always ready for its nightly rounds, run the self-contained tests:

1.  Navigate to the `utils/nightly-archive-auditor/` directory.
2.  Run the tests using `unittest`:

    ```bash
    python -m unittest tests/test_auditor.py
    ```

    All tests should pass, verifying the file scanning, age calculation, and report generation logic.
