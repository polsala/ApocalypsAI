import os
import shutil
import tarfile
import time
import datetime
import logging
from cryptography.fernet import Fernet

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def snapshot_and_encrypt(
    source_dir: str,
    dest_dir: str,
    encryption_key: bytes
) -> str:
    """Takes a snapshot of source_dir, encrypts it, and stores it in dest_dir."""
    if not os.path.isdir(source_dir):
        logging.error(f"Source directory not found: {source_dir}")
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    os.makedirs(dest_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_snapshot_dir = os.path.join("/tmp", f"snapshot_temp_{timestamp}")
    archive_name = f"snapshot_{timestamp}.tar.gz"
    archive_path = os.path.join("/tmp", archive_name)
    encrypted_file_path = os.path.join(dest_dir, f"{archive_name}.encrypted")

    fernet = Fernet(encryption_key)

    try:
        logging.info(f"Creating temporary snapshot of {source_dir} in {temp_snapshot_dir}")
        shutil.copytree(source_dir, temp_snapshot_dir)

        logging.info(f"Archiving {temp_snapshot_dir} to {archive_path}")
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(temp_snapshot_dir, arcname=os.path.basename(source_dir))

        logging.info(f"Encrypting {archive_path} to {encrypted_file_path}")
        with open(archive_path, "rb") as f:
            file_data = f.read()
        encrypted_data = fernet.encrypt(file_data)

        with open(encrypted_file_path, "wb") as f:
            f.write(encrypted_data)

        logging.info(f"Successfully created encrypted snapshot: {encrypted_file_path}")
        return encrypted_file_path
    except Exception as e:
        logging.error(f"Error during snapshot and encryption: {e}")
        raise
    finally:
        if os.path.exists(temp_snapshot_dir):
            shutil.rmtree(temp_snapshot_dir)
        if os.path.exists(archive_path):
            os.remove(archive_path)

def main():
    source_dir = os.environ.get("SOURCE_DIR")
    dest_dir = os.environ.get("DEST_DIR")
    encryption_key_str = os.environ.get("ENCRYPTION_KEY")
    interval_seconds = int(os.environ.get("INTERVAL_SECONDS", 3600))

    if not all([source_dir, dest_dir, encryption_key_str]):
        logging.error("Missing required environment variables: SOURCE_DIR, DEST_DIR, ENCRYPTION_KEY")
        exit(1)

    try:
        encryption_key = encryption_key_str.encode('utf-8')
        # Validate key format (Fernet key must be URL-safe base64 encoded)
        Fernet(encryption_key) 
    except Exception as e:
        logging.error(f"Invalid ENCRYPTION_KEY format: {e}")
        exit(1)

    logging.info(f"Chrono-Cache Guardian started. Source: {source_dir}, Dest: {dest_dir}, Interval: {interval_seconds}s")

    while True:
        try:
            snapshot_and_encrypt(source_dir, dest_dir, encryption_key)
        except Exception as e:
            logging.error(f"Failed to create snapshot: {e}")
        logging.info(f"Waiting for {interval_seconds} seconds until next snapshot...")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    main()
