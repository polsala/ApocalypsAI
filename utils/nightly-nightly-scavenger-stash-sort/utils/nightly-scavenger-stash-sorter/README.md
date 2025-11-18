# Nightly Scavenger's Stash Sorter

## Overview

In the desolate digital wasteland, your files can quickly become a chaotic mess of scavenged data. The `nightly-scavenger-stash-sorter` is here to bring order to the anarchy! This whimsical yet genuinely useful command-line utility helps you organize your files by automatically moving them into categorized subdirectories based on their file extensions.

Think of it as sorting your precious loot into designated bins: 'Documents', 'Images', 'Audio', 'Video', 'Archives', 'Executables', 'Code', and 'Other'.

## Features

*   **Automatic Categorization**: Files are sorted into predefined categories.
*   **Customizable Destination**: Choose where your sorted stash ends up.
*   **Duplicate Handling**: Automatically renames files if a duplicate exists in the destination category (e.g., `report.pdf` becomes `report_1.pdf`).
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## Usage

To run the Scavenger's Stash Sorter, navigate to the utility's directory and execute the `sorter.py` script with the required arguments.

```bash
python src/sorter.py --source /path/to/your/messy/stash --destination /path/to/your/organized/vault
```

### Arguments

*   `--source <path>`: **Required**. The path to the directory containing the files you want to sort.
*   `--destination <path>`: **Optional**. The path where the sorted category folders will be created. If not provided, a new directory named `sorted_stash` will be created inside the source directory.

### Example

Let's say you have a directory `/home/user/downloads` with various files:

```
/home/user/downloads/
├── report.pdf
├── vacation_pic.jpg
├── song.mp3
├── setup.exe
├── old_archive.zip
├── script.py
├── README.md
├── unknown_file
└── another_report.pdf
```

Running the sorter:

```bash
python src/sorter.py --source /home/user/downloads --destination /home/user/organized_files
```

After execution, your `/home/user/organized_files` directory will look like this:

```
/home/user/organized_files/
├── Documents/
│   ├── report.pdf
│   └── another_report.pdf
├── Images/
│   └── vacation_pic.jpg
├── Audio/
│   └── song.mp3
├── Archives/
│   └── old_archive.zip
├── Executables/
│   └── setup.exe
├── Code/
│   └── script.py
├── Other/
│   ├── README.md
│   └── unknown_file
```

## Categories & Extensions

The utility uses the following default categories and their associated file extensions:

*   **Documents**: `.txt`, `.pdf`, `.doc`, `.docx`, `.odt`, `.rtf`, `.md`
*   **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`
*   **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`
*   **Video**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`
*   **Archives**: `.zip`, `.tar`, `.gz`, `.rar`, `.7z`
*   **Executables**: `.exe`, `.sh`, `.bat`, `.app`
*   **Code**: `.py`, `.js`, `.html`, `.css`, `.java`, `.c`, `.cpp`, `.go`, `.rb`
*   **Other**: Any file not matching the above categories, or files without extensions.

## Development

This utility is written in Python 3.11 and uses only standard library modules. Contributions are welcome to expand categories or add new features!
