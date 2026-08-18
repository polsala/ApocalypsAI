# Nightly Chronosync Capsule

A containerized utility designed to preserve your precious digital artifacts against the ravages of temporal distortion and data decay. The Chronosync Capsule allows you to create encrypted, time-locked archives of directories, ensuring your legacies are safe until their designated "unlock" moment.

## Features

*   **Encrypted Archiving**: Securely compress and encrypt any directory using AES-256-CBC.
*   **Temporal Locking (Conceptual)**: Attach a future "unlock date" to your capsule, serving as a reminder for when its contents are meant to be revealed. This date is appended to the filename for human reference.
*   **Self-Contained**: Runs entirely within a Docker container, ensuring consistent operation across different environments.
*   **Simple Interface**: Easy-to-use command-line interface for creating and unlocking capsules.

## Usage

### 1. Build the Docker Image

Navigate to the `nightly-chronosync-capsule` directory and build the image:

```bash
docker build -t chronosync-capsule .
```

### 2. Create a Time Capsule

To archive and encrypt a directory, you'll need to mount it into the container. The capsule (the `.tar.enc` file) will be created in the current working directory on your host machine (specifically, the directory mounted to `/capsules`).

```bash
# Example: Archive a directory named 'my_precious_data'
# The capsule will be named 'my_precious_data_capsule_YYYYMMDD-HHMMSS_unlock-YYYYMMDD.tar.enc'
# Replace '/path/to/your/data' with the absolute path to your host directory.
# Replace 'your_secret_password' with a strong password.
# Replace '20251231' with your desired conceptual unlock date (optional, YYYYMMDD format).

docker run --rm \
  -v "$(pwd):/capsules" \
  -v "/path/to/your/data:/data" \
  -e CHRONOSYNC_PASSWORD="your_secret_password" \
  chronosync-capsule create /data my_precious_data_capsule --unlock-date 20251231
```

*   `-v "$(pwd):/capsules"`: Mounts your current host directory to `/capsules` inside the container. This is where the `.tar.enc` file will be saved.
*   `-v "/path/to/your/data:/data"`: Mounts the directory you want to archive from your host to `/data` inside the container. The path `/data` is what the container sees.
*   `-e CHRONOSYNC_PASSWORD="..."`: Sets the encryption password. **WARNING: For production use, consider more secure ways to pass secrets than environment variables in command history (e.g., Docker secrets or a secret management system).**
*   `create /data my_precious_data_capsule`: The command to create a capsule from `/data` (inside container) with a base name `my_precious_data_capsule`.
*   `--unlock-date YYYYMMDD`: (Optional) Specifies a conceptual unlock date. This is appended to the filename for human reference.

### 3. Unlock a Time Capsule

To decrypt and extract a capsule:

```bash
# Example: Unlock 'my_precious_data_capsule_20231027-103000_unlock-20251231.tar.enc'
# The contents will be extracted into a new directory named 'my_precious_data_capsule_unlocked' on your host.
# Replace 'your_secret_password' with the password used for encryption.

docker run --rm \
  -v "$(pwd):/capsules" \
  -v "$(pwd)/my_unlocked_data_capsule_unlocked:/output" \
  -e CHRONOSYNC_PASSWORD="your_secret_password" \
  chronosync-capsule unlock "/capsules/my_precious_data_capsule_20231027-103000_unlock-20251231.tar.enc" /output
```

*   `-v "$(pwd):/capsules"`: Mounts your current host directory (where the capsule is located) to `/capsules` inside the container.
*   `-v "$(pwd)/my_unlocked_data_capsule_unlocked:/output"`: Mounts a host directory where the extracted contents will be placed. The path `/output` is what the container sees.
*   `unlock "/capsules/my_capsule.tar.enc" /output`: The command to unlock the specified capsule (path inside container) and extract its contents into `/output` (inside container).

## Development & Testing

See the `tests/test_chronosync.sh` script for examples of how to test the utility locally.
