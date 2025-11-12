# Scavenger's Stash Organizer

## Bring Order to the Digital Wasteland!

In the chaotic aftermath, every byte of data is precious. The `scavenger-stash-organizer` is your trusty companion for sorting through the digital debris, categorizing your salvaged files, and identifying redundant copies that are just wasting precious storage space.

This utility helps you transform a messy collection of files from a chaotic source into a well-structured 'stash' of categorized data, making it easier to find what you need when the world depends on it.

## Features

*   **Automated Categorization**: Moves files into predefined category folders (e.g., `documents`, `images`, `archives`) within your chosen destination.
*   **Duplicate Detection**: Scans the *destination* directory for identical files based on their content hash, helping you reclaim valuable storage.
*   **Self-Contained**: No external network calls, operates entirely on your local filesystem.

## Usage

Run the utility from its `src` directory, providing a source directory to scan and a destination directory where your organized stash will be created.

```bash
python src/organizer.py <source_directory> <destination_directory>
```

### Arguments:

*   `<source_directory>`: The path to the directory containing the files you want to organize. Files will be moved *from* here.
*   `<destination_directory>`: The path where the organized category folders and files will be created. This directory will be created if it doesn't exist.

### Example:

```bash
# Organize files from './downloads' into './my_digital_stash'
python src/organizer.py ./downloads ./my_digital_stash
```

## File Categories

The organizer uses the following default categories based on file extensions:

*   `documents`: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.md`
*   `images`: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg`
*   `videos`: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.flv`
*   `audio`: `.mp3`, `.wav`, `.aac`, `.flac`, `.ogg`, `.m4a`
*   `archives`: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`
*   `executables`: `.exe`, `.dmg`, `.app`, `.sh`, `.bat` (Handle with care!)
*   `others`: Any file not matching the above categories.
