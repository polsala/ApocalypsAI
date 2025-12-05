import os
import shutil
import zipfile
import json
import hashlib
import datetime
import tempfile
import sys

def calculate_md5(filepath):
    """Calculates the MD5 hash of a file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def create_time_capsule(output_dir, *paths_to_archive):
    """
    Creates a timestamped zip archive (time capsule) of specified files/directories.
    Includes a manifest.json with original paths and MD5 hashes.
    """
    if not paths_to_archive:
        print("Error: No paths provided to archive.", file=sys.stderr)
        return None

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    capsule_name = f"time_capsule_{timestamp}"
    output_zip_path = os.path.join(output_dir, f"{capsule_name}.zip")

    # Create a temporary staging directory
    with tempfile.TemporaryDirectory() as staging_dir:
        manifest_data = {
            "creation_timestamp": datetime.datetime.now().isoformat(),
            "original_items": []
        }
        archived_count = 0

        for original_path in paths_to_archive:
            if not os.path.exists(original_path):
                print(f"Warning: Path not found - {original_path}. Skipping.", file=sys.stderr)
                continue

            # Determine the name inside the archive to avoid conflicts
            # and keep it simple (flat structure in staging for now)
            base_name = os.path.basename(original_path)
            archived_name = base_name
            counter = 1
            while os.path.exists(os.path.join(staging_dir, archived_name)):
                name_parts = os.path.splitext(base_name)
                archived_name = f"{name_parts[0]}_{counter}{name_parts[1]}"
                counter += 1

            destination_path = os.path.join(staging_dir, archived_name)

            if os.path.isfile(original_path):
                shutil.copy2(original_path, destination_path)
                md5_hash = calculate_md5(destination_path)
                size = os.path.getsize(destination_path)
                manifest_data["original_items"].append({
                    "original_path": os.path.abspath(original_path),
                    "archived_name": archived_name,
                    "type": "file",
                    "size_bytes": size,
                    "md5_hash": md5_hash
                })
                archived_count += 1
            elif os.path.isdir(original_path):
                shutil.copytree(original_path, destination_path)
                # For directories, we'll just record the directory itself.
                # Hashing individual files within a copied directory is more complex
                # and might be overkill for a manifest of the top-level items.
                # We can add a note about this in the manifest or skip hash for dirs.
                # For now, let's just record the directory entry.
                size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, fn in os.walk(destination_path) for f in fn)
                manifest_data["original_items"].append({
                    "original_path": os.path.abspath(original_path),
                    "archived_name": archived_name,
                    "type": "directory",
                    "size_bytes": size,
                    "md5_hash": "N/A" # MD5 for directory content is complex, not doing for now
                })
                archived_count += 1

        if archived_count == 0:
            print("No valid items found to archive. No time capsule created.", file=sys.stderr)
            return None

        # Write manifest.json to the staging directory
        manifest_path = os.path.join(staging_dir, "manifest.json")
        with open(manifest_path, 'w') as f:
            json.dump(manifest_data, f, indent=4)

        # Create the zip archive
        # shutil.make_archive creates a .zip, .tar, etc. It expects base_name and root_dir.
        # The base_name will be the full path to the archive without extension.
        # The root_dir is the directory to start archiving from.
        archive_base = os.path.join(output_dir, capsule_name)
        shutil.make_archive(archive_base, 'zip', staging_dir)

    print(f"Time capsule created: {output_zip_path}")
    return output_zip_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python src/time_capsule.py <path_to_item_1> [path_to_item_2] ...", file=sys.stderr)
        sys.exit(1)

    # Output the zip file to the current working directory
    output_directory = os.getcwd()
    create_time_capsule(output_directory, *sys.argv[1:])
