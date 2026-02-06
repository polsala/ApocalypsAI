# Nightly Digital Dust Sweeper

## "Sweep Away the Digital Dust Bunnies!"

In the post-apocalyptic digital landscape, forgotten files accumulate like dust bunnies in the corners of your hard drive, slowing down your systems and obscuring vital data. The `nightly-digital-dust-sweeper` is your trusty broom, designed to help you identify, quarantine, or even banish these digital relics.

This whimsical Node.js utility scans specified directories for files older than a given age, presenting them as 'digital dust bunnies' ready for a good sweep. Keep your digital shelter tidy and efficient!

## Features

*   **Age-based Scanning**: Find files older than a specified number of days.
*   **Recursive Search**: Dive deep into subdirectories to uncover hidden dust.
*   **Dry Run Mode**: Preview which files would be affected without making any changes.
*   **Quarantine Zone**: Move identified 'dust bunnies' to a designated directory for review, rather than immediate deletion.
*   **Direct Deletion**: For the brave, directly remove unwanted files.

## Installation

To install the `nightly-digital-dust-sweeper` globally, ensuring it's always ready for action:

```bash
npm install -g nightly-digital-dust-sweeper
```

## Usage

Run the sweeper from your terminal. You must provide a target path and an age threshold.

```bash
digital-dust-sweeper <path> --age <days> [options]
```

### Arguments

*   `<path>`: The root directory to start sweeping from. This can be an absolute or relative path.

### Options

*   `--age <days>` (required): Files older than this many days will be considered 'digital dust bunnies'.
*   `--dry-run`: Perform a scan and report findings without moving or deleting any files. Highly recommended for initial sweeps!
*   `--quarantine <directory>`: Move identified files to this specified directory instead of deleting them. The directory will be created if it doesn't exist.
*   `--delete`: Directly delete identified files. **Use with extreme caution!** This option overrides `--quarantine`.
*   `--help`: Display usage information.

## Examples

1.  **Dry run to see files older than 30 days in your current directory:**

    ```bash
    digital-dust-sweeper . --age 30 --dry-run
    ```

2.  **Quarantine files older than 90 days from your 'downloads' folder:**

    ```bash
    digital-dust-sweeper ~/Downloads --age 90 --quarantine ~/DigitalQuarantine
    ```

3.  **Directly delete files older than 7 days from a specific project folder (be careful!):**

    ```bash
    digital-dust-sweeper /var/log/old-archives --age 7 --delete
    ```

## Contributing

Got an idea for a new sweeping technique or a more efficient digital broom? Feel free to contribute to the `nightly-digital-dust-sweeper` project! Your efforts help keep the digital realm clean for all survivors.
