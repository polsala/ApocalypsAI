# Apocalypse Archive Auditor

## 📜 Description

In the grim darkness of the far future (or just a very cluttered hard drive), knowledge is power, and organized knowledge is survival! The Apocalypse Archive Auditor is a whimsical-yet-useful utility designed to help you make sense of your digital hoard. It scans a specified directory, categorizes files by their extensions, and flags "ancient" files that might be critical historical records, forgotten treasures, or just digital dust bunnies. Perfect for pre-apocalyptic data consolidation or post-apocalyptic digital archaeology!

## 🚀 Usage

This utility is a Python 3.11 script.

### Prerequisites

*   Python 3.11 or newer

### Running the Auditor

Navigate to the `src` directory and run the `auditor.py` script with your desired arguments.

```bash
python src/auditor.py <directory_path> [OPTIONS]
```

**Arguments:**

*   `<directory_path>`: The path to the directory you want to audit. This is a required argument.

**Options:**

*   `--extensions <ext1> <ext2> ...`: A space-separated list of file extensions to include in the audit (e.g., `.txt .md .pdf`). If this option is omitted, all files will be included.
*   `--age-threshold <years>`: An integer specifying the number of years. Files older than this threshold will be flagged as "old". Default is `5` years.

### Examples

1.  **Audit your entire "Important Documents" folder, including all file types:**
    ```bash
    python src/auditor.py /home/user/ImportantDocuments
    ```

2.  **Scan your "KnowledgeBase" for only text and markdown files, flagging anything older than 10 years:**
    ```bash
    python src/auditor.py /mnt/data/KnowledgeBase --extensions .txt .md --age-threshold 10
    ```

3.  **Check your "Photos" directory for any ancient image files (e.g., .jpg, .png) older than 7 years:**
    ```bash
    python src/auditor.py /media/photos --extensions .jpg .png --age-threshold 7
    ```

## 📊 Example Output

```
Audit complete for '/home/user/ImportantDocuments':
  Total files: 125
  Total size: 123.45 MB
  Files by extension: {'.pdf': 45, '.docx': 20, '.txt': 30, '.jpg': 25, '.xlsx': 5}
  Old files (>5 years): 12

--- Old Files Details ---
  - Path: /home/user/ImportantDocuments/old_contract.pdf, Age: 6.2 years, Last Modified: 2017-05-10T14:30:00
  - Path: /home/user/ImportantDocuments/ancient_photo.jpg, Age: 8.1 years, Last Modified: 2015-03-22T10:00:00
  - Path: /home/user/ImportantDocuments/subdir/forgotten_memo.txt, Age: 5.5 years, Last Modified: 2018-01-15T09:00:00
  # ... more old files
```
