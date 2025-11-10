# Nightly Data Ark Builder

## Prepare for the Inevitable: Archive Your Digital Legacy!

In these uncertain times, safeguarding your digital memories is paramount. The `Nightly Data Ark Builder` is a whimsical yet practical utility designed to help you create a robust, self-contained archive of your essential files and folders. Think of it as your personal digital time capsule, ready for off-world storage, your underground bunker, or simply a secure backup.

### Features

*   **Simple Archiving**: Easily zip up single files or entire directories.
*   **Manifest Included**: Every ark comes with a `MANIFEST.txt` detailing its contents and creation time.
*   **Self-Contained**: A single Python script, minimal dependencies (standard library only).
*   **Whimsical Naming**: Because even apocalypse prep can be fun!

### Usage

To build your data ark, simply run the `ark_builder.py` script from your terminal:

```bash
python src/ark_builder.py --source <path_to_file_or_folder_1> [path_to_file_or_folder_2 ...] --output <output_ark_name.zip>
```

**Arguments:**

*   `--source`: One or more paths to files or directories you wish to include in your data ark. You can specify multiple paths by separating them with spaces.
*   `--output`: The desired path and filename for your output `.zip` archive (e.g., `my_precious_memories.zip`).

### Examples

1.  **Archive a single file:**
    ```bash
    python src/ark_builder.py --source my_important_document.txt --output my_ark.zip
    ```

2.  **Archive an entire folder:**
    ```bash
    python src/ark_builder.py --source my_photos_folder/ --output photo_ark.zip
    ```

3.  **Archive multiple files and folders:**
    ```bash
    python src/ark_builder.py --source my_journal.md my_recipes/ family_photos/ --output ultimate_survival_ark.zip
    ```

### What's Inside the Ark?

The generated `.zip` file will contain all your specified files and folders, maintaining their relative structure. Additionally, a `MANIFEST.txt` file will be present at the root of the archive, listing all contents and providing metadata about the ark's creation.

Prepare wisely, for the future is unwritten... but your past can be archived!
