# Cosmic Dust Cleanup Crew

The ApocalypsAI Nightly Integrator presents the "Cosmic Dust Cleanup Crew" – your vigilant assistant for maintaining a pristine repository!

This utility scans a specified directory for common "cosmic dust" – temporary files, backup copies, cache directories, and other digital detritus that can accumulate over time. It helps you identify files that are likely safe to remove, keeping your project lean and your `git status` output clean.

**Important**: This tool is a *reporter*, not an *executor*. It will only list the files it identifies as "dust"; it will **never** delete or modify any files. You retain full control over what gets cleaned up.

## Usage

To run the Cosmic Dust Cleanup Crew, navigate to its directory and execute the `cleanup.py` script with the target path:

```bash
python src/cleanup.py /path/to/your/repository
```

If no path is provided, it will default to the current working directory.

## Example Output

```
Scanning /path/to/your/repository for cosmic dust...

Identified Cosmic Dust:
- /path/to/your/repository/src/main.py.bak
- /path/to/your/repository/temp_data.csv
- /path/to/your/repository/logs/app.log
- /path/to/your/repository/__pycache__/
- /path/to/your/repository/.DS_Store
- /path/to/your/repository/nested/file.txt~
```

Keep your digital cosmos sparkling!
