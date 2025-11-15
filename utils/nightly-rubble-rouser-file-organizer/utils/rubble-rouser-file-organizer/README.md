# Rubble-Rouser File Organizer

## Description
In the digital wasteland, files accumulate like forgotten relics. The Rubble-Rouser File Organizer is your trusty companion for sifting through the debris, categorizing your digital hoard, and bringing order to chaos. This utility scans a specified directory and intelligently moves files into type-specific subfolders, making your digital scavenging expeditions far more efficient.

## Features
- **Automated Sorting**: Categorizes files into common types like Documents, Images, Videos, Archives, Code, and more.
- **Customizable Categories**: Easily extend or modify the file type mappings.
- **Safe Operations**: Creates target directories if they don't exist and handles existing files gracefully by skipping duplicates.
- **Whimsical Logging**: Provides themed output to make your organizing feel like a true post-apocalyptic salvage operation.

## Installation
This utility is self-contained. Simply ensure you have Python 3.11+ installed.

## Usage
To organize files in a directory, run the `organizer.py` script with the path to the directory you wish to clean.

```bash
python src/organizer.py /path/to/your/messy/directory
```

### Example
If you have a directory `/home/user/downloads` with files like:
- `report.pdf`
- `vacation.jpg`
- `project.zip`
- `script.py`
- `song.mp3`

Running `python src/organizer.py /home/user/downloads` will create subdirectories and move files:

```
/home/user/downloads/
├── Documents/
│   └── report.pdf
├── Images/
│   └── vacation.jpg
├── Archives/
│   └── project.zip
├── Code/
│   └── script.py
├── Videos/
├── Audio/
│   └── song.mp3
└── Others/
    # (e.g., 'unknown.xyz' if it existed)
```

## Configuration (src/organizer.py)
You can modify the `FILE_CATEGORIES` dictionary within `src/organizer.py` to customize which file extensions belong to which category, or to add new categories.
