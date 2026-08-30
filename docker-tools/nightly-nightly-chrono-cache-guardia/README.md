# Nightly Chrono-Cache Guardian

## Overview

The `nightly-chrono-cache-guardian` is a whimsical-yet-critical utility designed to protect your most vital data from the ravages of time, digital decay, and unforeseen temporal anomalies. It operates as a self-contained Docker service that periodically takes snapshots of a specified source directory, encrypts them with a robust key, and stores them in a designated destination directory.

Think of it as your personal digital time capsule, secured against the chaotic whims of the post-apocalyptic digital landscape.

## Features

*   **Automated Snapshots**: Periodically archives a source directory.
*   **Robust Encryption**: Uses `cryptography.fernet` for strong symmetric encryption.
*   **Timestamped Archives**: Each snapshot is named with a timestamp for easy retrieval and versioning.
*   **Containerized**: Easy deployment and isolation using Docker.
*   **Configurable**: Source, destination, encryption key, and interval are configurable via environment variables.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-chrono-cache-guardian` directory and build the image:

```bash
docker build -t chrono-cache-guardian .
```

### 2. Prepare Your Environment

You'll need:

*   A **source directory** on your host machine that you want to protect.
*   A **destination directory** on your host machine where encrypted archives will be stored.
*   An **encryption key**. This is crucial! Generate a new one using Python:
    ```python
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    print(key.decode()) # Keep this key SAFE!
    ```
    The output will be a URL-safe base64 encoded key. Store it securely.

### 3. Run the Guardian Service

Run the Docker container, mapping your host directories and providing environment variables:

```bash
docker run -d \
  --name chrono-guardian \
  -v /path/to/your/source/data:/app/source_data:ro \
  -v /path/to/your/destination/archives:/app/dest_archives:rw \
  -e SOURCE_DIR="/app/source_data" \
  -e DEST_DIR="/app/dest_archives" \
  -e ENCRYPTION_KEY="<YOUR_GENERATED_FERNET_KEY>" \
  -e INTERVAL_SECONDS="3600" \ # Snapshot every hour (3600 seconds)
  chrono-cache-guardian
```

**Replace the placeholders:**
*   `/path/to/your/source/data`: The absolute path to the directory you want to snapshot.
*   `/path/to/your/destination/archives`: The absolute path where encrypted archives will be saved.
*   `<YOUR_GENERATED_FERNET_KEY>`: The encryption key you generated.
*   `INTERVAL_SECONDS`: The frequency of snapshots in seconds (e.g., 60 for every minute, 3600 for every hour).

### 4. Verify Operation

Check the container logs to ensure it's running correctly:

```bash
docker logs chrono-guardian
```

You should see messages indicating snapshots are being taken and encrypted.

Periodically check your `/path/to/your/destination/archives` directory for new `.tar.gz.encrypted` files.

### 5. Decrypting an Archive

To decrypt and extract an archive, you'll need the original `ENCRYPTION_KEY` and a small Python script:

```python
from cryptography.fernet import Fernet
import tarfile
import os

ENCRYPTION_KEY = b"<YOUR_GENERATED_FERNET_KEY>" # Must be bytes!
ENCRYPTED_FILE_PATH = "/path/to/your/destination/archives/snapshot_YYYYMMDD_HHMMSS.tar.gz.encrypted"
OUTPUT_DIR = "/path/to/extract/to"

fernet = Fernet(ENCRYPTION_KEY)

with open(ENCRYPTED_FILE_PATH, "rb") as f:
    encrypted_data = f.read()

decrypted_data = fernet.decrypt(encrypted_data)

# Save decrypted data to a temporary tar.gz file
temp_tar_path = ENCRYPTED_FILE_PATH.replace(".encrypted", ".decrypted.tar.gz")
with open(temp_tar_path, "wb") as f:
    f.write(decrypted_data)

# Extract the tar.gz file
with tarfile.open(temp_tar_path, "r:gz") as tar:
    tar.extractall(path=OUTPUT_DIR)

os.remove(temp_tar_path) # Clean up temporary decrypted tarball
print(f"Archive extracted to {OUTPUT_DIR}")
```

## Configuration

The following environment variables can be set when running the Docker container:

*   `SOURCE_DIR` (required): The path inside the container to the directory to be snapshotted.
*   `DEST_DIR` (required): The path inside the container where encrypted archives will be stored.
*   `ENCRYPTION_KEY` (required): The URL-safe base64 encoded Fernet key for encryption.
*   `INTERVAL_SECONDS` (optional, default: `3600`): The interval in seconds between snapshots.

## Development & Testing

See the `tests/` directory for how to run automated tests.
