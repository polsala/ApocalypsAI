# Digital Dust Bunny Collector

## 🧹 What is it?

The Digital Dust Bunny Collector is a whimsical utility designed to help you declutter your digital spaces. It scans a specified directory for files and folders that haven't been touched in a while, identifying them as 'digital dust bunnies' – forgotten bits of data accumulating over time. Think of it as a friendly robot vacuum for your hard drive, but instead of sucking up physical dust, it reports on digital detritus.

## ✨ Why is it useful?

*   **Reclaim Space**: Identify large, old files that are hogging disk space.
*   **Improve Organization**: Pinpoint forgotten projects or downloads that can be archived or deleted.
*   **Boost Performance**: While not directly speeding up your system, a cleaner drive can contribute to better overall digital hygiene.
*   **Whimsical Fun**: Who knew cleaning could be so entertaining?

## 🚀 How to Use

Run the `collector.py` script with the target directory and an optional maximum age in days.

```bash
python3 src/collector.py --path /path/to/scan --max-age-days 365
```

**Arguments:**
*   `--path <directory>`: The directory to scan for digital dust bunnies. (Required)
*   `--max-age-days <int>`: Files and directories older than this many days will be reported. Defaults to 365 days. (Optional)

## 📊 Example Output

```
Scanning /home/user/documents for digital dust bunnies older than 365 days...

Found 🧹 Digital Dust Bunnies 🧹:

- File: /home/user/documents/old_project/legacy_code.py (Size: 1.2 KB, Last Modified: 2022-01-15)
- File: /home/user/documents/downloads/ancient_archive.zip (Size: 50.5 MB, Last Modified: 2021-03-20)
- Dir:  /home/user/documents/forgotten_folder/ (Last Modified: 2022-02-01)

--- Summary ---
Total Digital Dust Bunnies Found: 3
Total Size of Files: 50.5 MB
```

## 🧪 How to Test

To run the automated tests, navigate to the `utils/digital-dust-bunny-collector` directory and execute:

```bash
python3 -m unittest tests/test_collector.py
```
