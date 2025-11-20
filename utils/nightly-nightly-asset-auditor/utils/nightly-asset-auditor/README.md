# Nightly Asset Auditor

## 📜 Description

In the chaotic aftermath, digital assets are often overlooked. The **Nightly Asset Auditor** is your personal sentinel, designed to help you meticulously track and audit your crucial digital possessions – be it vital documents, cherished memories, software licenses, or secret survival plans. It ensures that even when the world crumbles, your digital legacy remains organized and accessible.

## 🛠️ Usage

### Prerequisites

*   Python 3.8+

### Installation

No installation needed! Just navigate to the `src/` directory.

### Running the Auditor

The auditor operates on a JSON file (`assets.json` by default) where your assets are stored.

```bash
python src/auditor.py --help
```

**Example Commands:**

1.  **Initialize a new asset store (if `assets.json` doesn't exist):**
    ```bash
    python src/auditor.py init
    ```

2.  **Add a new asset:**
    ```bash
    python src/auditor.py add \
        --name "Emergency Contact List" \
        --type "Document" \
        --path-or-url "/vault/docs/contacts.pdf" \
        --description "Scanned list of pre-apocalypse contacts" \
        --backup-location "USB Drive Alpha"
    ```

3.  **List all assets:**
    ```bash
    python src/auditor.py list
    ```

4.  **Mark an asset as audited (by name):**
    ```bash
    python src/auditor.py audit --name "Emergency Contact List"
    ```

5.  **Find assets not audited in the last X days (e.g., 30 days):**
    ```bash
    python src/auditor.py stale --days 30
    ```

6.  **Update an existing asset (by name):**
    ```bash
    python src/auditor.py update \
        --name "Emergency Contact List" \
        --new-path-or-url "/vault/docs/contacts_v2.pdf" \
        --new-backup-location "Cloud Storage Omega"
    ```

## 📂 Asset Structure

Each asset is stored as a JSON object with the following fields:

*   `name` (string): Unique identifier for the asset.
*   `type` (string): Category (e.g., "Document", "Software License", "Photo Album", "URL").
*   `path_or_url` (string): File path, folder path, or URL where the asset resides.
*   `description` (string): A brief explanation of the asset.
*   `backup_location` (string): Where the asset is backed up (e.g., "USB Drive Alpha", "Cloud Storage Omega", "Encrypted SSD").
*   `last_audited` (string, ISO 8601 datetime): Timestamp of the last audit. Automatically set on creation and update.

## 🧪 Tests

To run the tests, navigate to the `tests/` directory and execute:

```bash
python -m unittest discover
```
