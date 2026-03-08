# Nightly Digital Dust Bunny Sweeper

## Overview
In the vast, ever-expanding digital wasteland, files accumulate like forgotten relics. Some are cherished, some are vital, and some... well, some are just 'digital dust bunnies'. These are the files that haven't been touched in ages, silently occupying space and perhaps whispering forgotten secrets.

The `nightly-digital-dust-bunny-sweeper` is a whimsical Node.js utility designed to help you identify these digital dust bunnies. It scans a specified directory for files older than a given number of days, reporting their paths and last modification times. It's your first step towards a cleaner, more organized digital sanctuary.

## Features
*   **Recursive Scanning**: Traverses subdirectories to find hidden dust bunnies.
*   **Age-Based Filtering**: Easily specify how old a file must be to be considered a dust bunny.
*   **Clear Reporting**: Lists identified files with their full paths and last modification dates.
*   **Whimsical Output**: Adds a touch of fun to the mundane task of file cleanup.

## Installation
1.  Ensure you have Node.js (v18 or higher recommended) installed.
2.  Clone the ApocalypsAI repository or navigate to this utility's directory.
3.  No external `npm` dependencies are required; it uses built-in Node.js modules.

## Usage
Run the utility from your terminal, providing the target directory path and the age threshold in days.

```bash
node src/index.js <directory_path> <days_old>
```

### Arguments
*   `<directory_path>`: The absolute or relative path to the directory you want to sweep for dust bunnies.
*   `<days_old>`: An integer representing the minimum age (in days) for a file to be considered a 'digital dust bunny'. Files modified *before* this threshold will be reported.

### Examples

**1. Find files older than 365 days in your current project directory:**
```bash
node src/index.js . 365
```

**2. Find files older than 90 days in your documents folder:**
```bash
node src/index.js /home/user/Documents 90
```

**3. Find files older than 7 days in a temporary directory:**
```bash
node src/index.js /tmp/my_temp_files 7
```

## Output
The utility will print a list of all identified digital dust bunnies, along with their last modification dates. If no dust bunnies are found, it will let you know your digital space is sparkling clean!

```
Sweeping for digital dust bunnies older than 365 days in: /home/user/my_project

Found these forgotten digital dust bunnies:
- /home/user/my_project/old_report.pdf (Last modified: 2022-01-15T10:30:00.000Z)
- /home/user/my_project/archive/ancient_script.sh (Last modified: 2021-11-20T14:00:00.000Z)

Consider giving them a new home in the archive, or perhaps a gentle sweep into the void!
```

## Development & Testing
To run the tests for this utility, use Node.js's built-in test runner:

```bash
node --test tests/test.js
```

Tests are designed to be deterministic and offline, using mocks for file system operations to ensure reliability and speed.
