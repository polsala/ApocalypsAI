# Nightly Digital Dust Bunny Sweeper

## Summary
The Nightly Digital Dust Bunny Sweeper is a whimsical-yet-useful containerized utility designed to help you identify and report on digital clutter. It scans a specified directory for files older than a given number of days and for empty directories, presenting its findings as "digital dust bunnies" that might need sweeping. It's a safe, read-only tool that only reports, never deletes.

## Usage

1.  **Build the Docker image (optional, or pull if available):**
    ```bash
    docker build -t digital-dust-bunny-sweeper .
    ```

2.  **Run the sweeper:**
    Mount the directory you want to scan as a volume to `/scan_target` inside the container.
    Specify the `--path` argument to point to this mounted directory (which will be `/scan_target`).
    Use `--days_old` to define what constitutes an "old" file.

    ```bash
    docker run --rm \
      -v /path/to/your/local/directory:/scan_target \
      digital-dust-bunny-sweeper \
      --path /scan_target \
      --days_old 90
    ```
    Replace `/path/to/your/local/directory` with the actual path on your host machine you wish to scan.

    **Example:** Scan your home directory for files older than 180 days and empty folders:
    ```bash
    docker run --rm \
      -v $HOME:/scan_target \
      digital-dust-bunny-sweeper \
      --path /scan_target \
      --days_old 180
    ```

    **Arguments:**
    *   `--path <directory>`: The absolute path to the directory to scan *inside the container*. (Required)
    *   `--days_old <number>`: Files older than this many days will be reported as "dust bunnies". (Default: 90)
    *   `--no_empty_dirs`: Skip scanning for empty directories. (Optional flag)

## Example Output

```
⚠️ Initiating Digital Dust Bunny Sweep in /scan_target... ⚠️

Scanning for files older than 90 days...
Scanning for empty directories...

✨ Digital Dust Bunny Report ✨

Found 3 ancient scrolls (files older than 90 days):
  - /scan_target/old_project/legacy_code.py (Last modified: 2023-01-15)
  - /scan_target/downloads/temp_report.pdf (Last modified: 2023-03-20)
  - /scan_target/archive/forgotten_memo.txt (Last modified: 2022-11-01)

Found 2 desolate caverns (empty directories):
  - /scan_target/empty_folder_a
  - /scan_target/project_x/build/temp

Total Digital Dust Bunnies: 5
Consider tidying up to prevent a data-apocalypse!
```

## Development & Testing

To run tests, you'll need Python 3.9+ and `unittest` (or `pytest`).
```bash
# From the root of the utility directory
pip install -r requirements.txt
python -m unittest tests/test_dust_bunny_sweeper.py
```
