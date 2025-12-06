import argparse
import hashlib
import os

CHUNK_SIZE = 65536  # 64KB

def calculate_file_checksum(filepath: str, algorithm: str = 'sha256') -> str:
    """
    Calculates the checksum of a single file using the specified algorithm.
    """
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        return f"ERROR: File not found: {filepath}"
    except Exception as e:
        return f"ERROR: Could not process {filepath}: {e}"

def calculate_directory_checksums(directory_path: str, algorithm: str = 'sha256') -> dict[str, str]:
    """
    Recursively calculates checksums for all files in a directory.
    Returns a dictionary mapping file paths to their checksums.
    """
    results = {}
    file_count = 0
    if not os.path.isdir(directory_path):
        return {directory_path: f"ERROR: Not a directory: {directory_path}"}

    print(f"Calculating checksums for: {directory_path}\n")

    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            checksum = calculate_file_checksum(filepath, algorithm)
            results[filepath] = checksum
            file_count += 1
            print(f"File: {filepath}\n  {algorithm.upper()}: {checksum}\n")
    
    print(f"Summary: {file_count} files processed.")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Calculate SHA256 checksums for files or directories."
    )
    parser.add_argument(
        '--path', 
        type=str, 
        required=True, 
        help='Path to the file or directory to process.'
    )
    parser.add_argument(
        '--algorithm', 
        type=str, 
        default='sha256', 
        help='Hashing algorithm to use (e.g., sha256, md5). Default: sha256.'
    )

    args = parser.parse_args()

    if os.path.isfile(args.path):
        print(f"Calculating checksum for: {args.path}\n")
        checksum = calculate_file_checksum(args.path, args.algorithm)
        print(f"File: {args.path}\n  {args.algorithm.upper()}: {checksum}")
    elif os.path.isdir(args.path):
        calculate_directory_checksums(args.path, args.algorithm)
    else:
        print(f"Error: Path '{args.path}' does not exist or is not a file/directory.")

if __name__ == '__main__':
    main()
