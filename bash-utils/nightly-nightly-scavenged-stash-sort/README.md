# Nightly Scavenged Stash Sorter

## Overview
In the chaotic aftermath, keeping your digital scavenged loot organized is paramount. The `nightly-scavenged-stash-sorter` is a whimsical yet practical bash utility designed to help you categorize and manage your files, ensuring that your vital data is neatly tucked away in its proper place. It scans a source directory, classifies files based on their extensions, moves them into corresponding category directories, and generates a comprehensive manifest of your newly organized stash.

## Features
- **Automated Classification**: Sorts files into predefined categories like `documents`, `images`, `archives`, `scripts`, `data`, `audio`, `video`, and `unknown`.
- **Manifest Generation**: Creates a `stash_manifest.txt` file detailing the original and new locations of all sorted files.
- **Customizable Destination**: Allows specifying a custom root directory for your sorted stash.
- **Whimsical Naming**: Embrace the post-apocalyptic theme with 'scavenged loot' and 'organized vault' concepts.

## Usage

```bash
./src/stash_sorter.sh <source_directory> [destination_root_directory]
```

- `<source_directory>`: The path to the directory containing the files you wish to sort (your 'scavenged loot').
- `[destination_root_directory]`: (Optional) The path where the categorized directories and manifest will be created (your 'organized vault'). If not provided, it defaults to `./sorted_stash` in the current working directory.

### Example

Let's say you have a directory named `my_loot` with various files:

```
my_loot/
├── report.pdf
├── photo.jpg
├── backup.zip
├── script.sh
├── notes.txt
└── unknown.xyz
```

To sort these files into a new directory called `my_vault`:

```bash
./src/stash_sorter.sh ./my_loot ./my_vault
```

After execution, `my_vault` will contain:

```
my_vault/
├── archives/
│   └── backup.zip
├── documents/
│   ├── report.pdf
│   └── notes.txt
├── images/
│   └── photo.jpg
├── scripts/
│   └── script.sh
├── unknown/
│   └── unknown.xyz
└── stash_manifest.txt
```

And `stash_manifest.txt` will list the sorted files.

## Categories
The script currently supports the following categories and their associated file extensions:

- **documents**: `txt`, `docx`, `pdf`, `md`, `rtf`
- **images**: `jpg`, `jpeg`, `png`, `gif`, `bmp`, `tiff`, `webp`
- **archives**: `zip`, `tar`, `gz`, `bz2`, `xz`, `rar`, `7z`
- **scripts**: `sh`, `py`, `js`, `rb`, `pl`
- **data**: `csv`, `json`, `xml`, `yml`, `yaml`
- **audio**: `mp3`, `wav`, `ogg`, `flac`
- **video**: `mp4`, `avi`, `mkv`, `mov`
- **unknown**: Any file with an unrecognized extension or no extension.

## Dependencies
- Bash (version 4.0 or higher recommended)
- Standard core utilities (`find`, `basename`, `mv`, `mkdir`, `echo`, `grep`)

## Development
Feel free to extend the categories or add new sorting logic to better suit your post-apocalyptic data management needs!
