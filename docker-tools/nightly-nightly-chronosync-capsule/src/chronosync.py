import os
import subprocess
import sys
import datetime
import argparse

def create_capsule(source_dir, output_base_name, password, unlock_date=None):
    """Creates an encrypted time capsule."""
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    unlock_suffix = f"_unlock-{unlock_date}" if unlock_date else ""
    output_filename = f"{output_base_name}_{timestamp}{unlock_suffix}.tar.enc"

    print(f"Creating archive from '{source_dir}'...")

    try:
        # Step 1: Create tar archive and pipe its stdout
        # tar -C <parent_of_source_dir> -cf - <source_dir_basename>
        tar_process = subprocess.Popen(
            ["tar", "-C", os.path.dirname(source_dir), "-cf", "-", os.path.basename(source_dir)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Step 2: Encrypt tar's stdout using openssl and write to file
        # openssl aes-256-cbc -pbkdf2 -salt -out <output_filename> -pass env:CHRONOSYNC_PASSWORD
        openssl_cmd = [
            "openssl", "aes-256-cbc", "-pbkdf2", "-salt",
            "-out", output_filename,
            "-pass", "env:CHRONOSYNC_PASSWORD" # Password from env var
        ]
        openssl_process = subprocess.Popen(
            openssl_cmd,
            stdin=tar_process.stdout,
            stdout=subprocess.PIPE, # Capture stdout for openssl (usually empty for -out)
            stderr=subprocess.PIPE
        )

        tar_process.stdout.close() # Allow tar_process to receive a SIGPIPE if openssl exits

        # Wait for both processes to complete and capture their outputs
        openssl_stdout, openssl_stderr = openssl_process.communicate()
        tar_stdout, tar_stderr = tar_process.communicate() # tar_stdout should be empty

        if tar_process.returncode != 0:
            print(f"Error during tar creation (exit code {tar_process.returncode}): {tar_stderr.decode().strip()}", file=sys.stderr)
            sys.exit(1)
        if openssl_process.returncode != 0:
            print(f"Error during encryption (exit code {openssl_process.returncode}): {openssl_stderr.decode().strip()}", file=sys.stderr)
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: Command not found. Make sure 'tar' and 'openssl' are installed. ({e})", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during archiving/encryption: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Time capsule '{output_filename}' created successfully.")

def unlock_capsule(capsule_path, output_dir, password):
    """Unlocks and extracts an encrypted time capsule."""
    if not os.path.isfile(capsule_path):
        print(f"Error: Capsule file '{capsule_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    print(f"Unlocking capsule '{capsule_path}' into '{output_dir}'...")

    try:
        # Step 1: Decrypt capsule file and pipe its stdout
        # openssl aes-256-cbc -pbkdf2 -d -salt -in <capsule_path> -pass env:CHRONOSYNC_PASSWORD
        openssl_cmd = [
            "openssl", "aes-256-cbc", "-pbkdf2", "-d", "-salt",
            "-in", capsule_path,
            "-pass", "env:CHRONOSYNC_PASSWORD" # Password from env var
        ]
        openssl_process = subprocess.Popen(
            openssl_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Step 2: Extract decrypted tar stream from openssl's stdout
        # tar -C <output_dir> -xf -
        tar_cmd = ["tar", "-C", output_dir, "-xf", "-"]
        tar_process = subprocess.Popen(
            tar_cmd,
            stdin=openssl_process.stdout,
            stdout=subprocess.PIPE, # Capture stdout for tar (usually empty)
            stderr=subprocess.PIPE
        )

        openssl_process.stdout.close() # Allow openssl_process to receive a SIGPIPE if tar exits

        # Wait for both processes to complete and capture their outputs
        tar_stdout, tar_stderr = tar_process.communicate()
        openssl_stdout, openssl_stderr = openssl_process.communicate()

        if openssl_process.returncode != 0:
            print(f"Error during decryption (exit code {openssl_process.returncode}): {openssl_stderr.decode().strip()}", file=sys.stderr)
            sys.exit(1)
        if tar_process.returncode != 0:
            print(f"Error during extraction (exit code {tar_process.returncode}): {tar_stderr.decode().strip()}", file=sys.stderr)
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: Command not found. Make sure 'tar' and 'openssl' are installed. ({e})", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during decryption/extraction: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Time capsule unlocked successfully into '{output_dir}'.")

def main():
    parser = argparse.ArgumentParser(
        description="Chronosync Capsule: Create and unlock encrypted time capsules.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser(
        "create",
        help="Create an encrypted time capsule from a directory.",
        epilog="""
Examples:
  # Archive /data into my_capsule_YYYYMMDD-HHMMSS.tar.enc
  chronosync.py create /data my_capsule

  # Archive /data with an unlock date of 2025-12-31
  chronosync.py create /data my_capsule --unlock-date 20251231
"""
    )
    create_parser.add_argument("source_dir", help="Path to the directory to archive (inside container).")
    create_parser.add_argument("output_base_name", help="Base name for the output capsule file (e.g., 'my_data_archive').")
    create_parser.add_argument("--unlock-date", help="Optional: Conceptual unlock date (YYYYMMDD). Appended to filename.")

    # Unlock command
    unlock_parser = subparsers.add_parser(
        "unlock",
        help="Unlock and extract an encrypted time capsule.",
        epilog="""
Examples:
  # Unlock my_capsule.tar.enc into my_unlocked_data/
  chronosync.py unlock my_capsule.tar.enc my_unlocked_data
"""
    )
    unlock_parser.add_argument("capsule_path", help="Path to the encrypted capsule file (.tar.enc).")
    unlock_parser.add_argument("output_dir", help="Directory where the contents will be extracted.")

    args = parser.parse_args()

    password = os.getenv("CHRONOSYNC_PASSWORD")
    if not password:
        print("Error: CHRONOSYNC_PASSWORD environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    if args.command == "create":
        create_capsule(args.source_dir, args.output_base_name, password, args.unlock_date)
    elif args.command == "unlock":
        unlock_capsule(args.capsule_path, args.output_dir, password)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
