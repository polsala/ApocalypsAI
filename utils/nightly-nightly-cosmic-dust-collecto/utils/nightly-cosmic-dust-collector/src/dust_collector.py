import os
import shutil
import argparse
import sys

def collect_dust(
    scan_path: str,
    max_size_bytes: int,
    allowed_extensions: list[str],
    mode: str,
    quarantine_dir: str,
    output_stream=sys.stdout # For testing print output
) -> list[str]:
    """
    Scans a directory for 'dust' files based on size and extension criteria.
    Can either list the files or move them to a quarantine directory.

    Args:
        scan_path: The root directory to start scanning from.
        max_size_bytes: Maximum file size in bytes to consider as 'dust'.
        allowed_extensions: List of file extensions to include. If empty, all files matching size are considered.
        mode: 'list' to print files, 'quarantine' to move them.
        quarantine_dir: Directory to move files to in 'quarantine' mode.
        output_stream: Stream to print output to (defaults to stdout).

    Returns:
        A list of paths to the files that were processed (listed or quarantined).
    """
    dust_files = []
    if mode == 'quarantine' and not os.path.exists(quarantine_dir):
        os.makedirs(quarantine_dir, exist_ok=True)
        output_stream.write(f"Created quarantine directory: {quarantine_dir}\n")

    for root, _, files in os.walk(scan_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                if file_size <= max_size_bytes:
                    is_dust = False
                    if not allowed_extensions: # No specific extensions, just size
                        is_dust = True
                    else:
                        # Check if file extension matches any in the allowed list
                        _, ext = os.path.splitext(file_path)
                        if ext.lower() in [e.lower() for e in allowed_extensions]:
                            is_dust = True

                    if is_dust:
                        dust_files.append(file_path)
                        if mode == 'list':
                            output_stream.write(f"[DUST] {file_path} ({file_size} bytes)\n")
                        elif mode == 'quarantine':
                            # Ensure the target directory structure is preserved under quarantine
                            relative_path = os.path.relpath(file_path, scan_path)
                            target_dir = os.path.join(quarantine_dir, os.path.dirname(relative_path))
                            os.makedirs(target_dir, exist_ok=True)
                            target_path = os.path.join(target_dir, os.path.basename(file_path))
                            shutil.move(file_path, target_path)
                            output_stream.write(f"[QUARANTINED] {file_path} -> {target_path}\n")
            except FileNotFoundError:
                output_stream.write(f"Warning: File not found during scan: {file_path}\n")
            except Exception as e:
                output_stream.write(f"Error processing {file_path}: {e}\n")

    if not dust_files:
        output_stream.write("No cosmic dust found! Your repository is sparkling clean.\n")
    return dust_files


def main():
    parser = argparse.ArgumentParser(
        description="Nightly Cosmic Dust Collector: Scans for small, forgotten files."
    )
    parser.add_argument(
        "--path",
        type=str,
        required=True,
        help="The root directory to start scanning from."
    )
    parser.add_argument(
        "--size",
        type=int,
        default=1024,
        help="Maximum file size in bytes to consider as 'dust' (default: 1024 bytes)."
    )
    parser.add_argument(
        "--extensions",
        nargs='*',
        default=[],
        help="Space-separated list of file extensions (e.g., .log .tmp) to include. "
             "If not specified, all files matching the size criteria are considered."
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=['list', 'quarantine'],
        default='list',
        help="Operation mode. 'list' will print files; 'quarantine' will move them (default: list)."
    )
    parser.add_argument(
        "--quarantine-dir",
        type=str,
        default='quarantine_dust',
        help="Directory to move files to in 'quarantine' mode. Will be created if it doesn't exist (default: quarantine_dust)."
    )

    args = parser.parse_args()

    collect_dust(
        scan_path=args.path,
        max_size_bytes=args.size,
        allowed_extensions=args.extensions,
        mode=args.mode,
        quarantine_dir=args.quarantine_dir
    )


if __name__ == "__main__":
    main()
