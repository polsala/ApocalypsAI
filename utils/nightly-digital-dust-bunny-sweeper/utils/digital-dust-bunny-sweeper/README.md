# Digital Dust Bunny Sweeper

## 🧹 What is this?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you tidy up your digital workspace. It scans specified directories for "digital dust bunnies" – those forgotten, empty folders, and temporary files that accumulate over time, cluttering your system and making it harder to find what you need. Think of it as a friendly robot vacuum for your file system!

## ✨ Features

*   **Empty Directory Detection**: Identifies directories that contain no files or subdirectories.
*   **Temporary File Spotting**: Locates files matching common temporary or log file patterns (e.g., `.tmp`, `.log`, `~`, `__pycache__`).
*   **Actionable Suggestions**: Provides a clear list of identified "dust bunnies" and suggests paths for deletion.
*   **Safe & Non-Destructive**: Only *suggests* deletions; it never deletes anything itself. You're always in control!

## 🚀 How to Use

1.  **Navigate**: Change into the `utils/digital-dust-bunny-sweeper/` directory.
2.  **Run**: Execute the `sweeper.py` script with the path you want to clean.

    ```bash
    python src/sweeper.py --path /path/to/your/messy/directory
    ```

    You can also specify multiple paths:

    ```bash
    python src/sweeper.py --path /path/to/project1 /path/to/downloads
    ```

## ⚙️ Configuration

Currently, the utility uses a predefined list of temporary file patterns. Future versions might allow custom patterns.

## 🧪 Testing

To run the tests for the Digital Dust Bunny Sweeper:

1.  **Navigate**: Change into the `utils/digital-dust-bunny-sweeper/` directory.
2.  **Run Tests**:

    ```bash
    python -m unittest tests/test_sweeper.py
    ```

## 🤝 Contributing

Feel free to suggest new "dust bunny" detection rules or features!
