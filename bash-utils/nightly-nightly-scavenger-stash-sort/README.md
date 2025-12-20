# Nightly Scavenger's Stash Sorter

## Overview

In the desolate wastes, every scrap counts. The `nightly-scavenger-stash-sorter` is a crucial utility for any survivor looking to bring order to their chaotic hauls. This bash script automatically sifts through a specified directory, identifying common types of "loot" (files) and organizing them into designated subdirectories like `Documents`, `Images`, `Archives`, `Executables`, and `Other`. No more rummaging through piles of unsorted findings – let the Stash Sorter bring method to your madness!

## Usage

To sort your scavenger's stash, simply run the script with the path to your target directory:

```bash
./src/sort_stash.sh /path/to/your/stash
```

### Arguments

*   `<directory_path>`: The absolute or relative path to the directory containing the files you wish to sort.

### Examples

Sort the current directory:
```bash
./src/sort_stash.sh .
```

Sort a specific stash:
```bash
./src/sort_stash.sh ~/my_apocalyptic_loot/
```

## How it Works

The script categorizes files based on their extensions:

*   **Documents**: `.txt`, `.md`, `.pdf`, `.doc`, `.docx`, `.odt`
*   **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`
*   **Archives**: `.zip`, `.tar`, `.gz`, `.rar`, `.7z`
*   **Executables**: `.sh`, `.run`, `.bin`, `.exe`
*   **Other**: Any file not matching the above categories.

It creates these category subdirectories if they don't already exist and moves the respective files into them.

## Whimsical Lore

"The winds whisper tales of survivors lost in their own clutter, unable to find that critical schematic or a precious photo amidst the rubble. Fear not, fellow wanderer! The ApocalypsAI Nightly Integrator presents the Scavenger's Stash Sorter, a digital companion to bring order to the chaos. Let your digital inventory be as pristine as a pre-fall library, even if the world outside is anything but."
