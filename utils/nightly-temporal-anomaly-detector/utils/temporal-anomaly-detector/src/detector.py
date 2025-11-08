import os
import datetime
import argparse

def find_future_files(directories, current_time=None):
    """
    Scans specified directories for files with modification times in the future.

    Args:
        directories (list): A list of directory paths to scan.
        current_time (datetime.datetime, optional): The current time to compare against.
                                                    Defaults to datetime.datetime.now() if None.

    Returns:
        list: A list of file paths that have future modification times.
    """
    if current_time is None:
        current_time = datetime.datetime.now()

    future_files = []
    current_timestamp = current_time.timestamp()

    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: Directory not found or not a directory: {directory}")
            continue

        for root, _, files in os.walk(directory):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    mtime = os.path.getmtime(file_path)
                    if mtime > current_timestamp:
                        future_files.append(file_path)
                except OSError as e:
                    print(f"Error accessing file {file_path}: {e}")
    return future_files

def main():
    parser = argparse.ArgumentParser(
        description="Scan directories for files with future modification times."
    )
    parser.add_argument(
        "directories",
        metavar="DIR",
        type=str,
        nargs=":", # Use ':' to allow 0 or more arguments, then check if empty
        help="One or more directories to scan. Defaults to current directory if none provided."
    )
    args = parser.parse_args()

    target_directories = args.directories if args.directories else ['.']

    print(f"Scanning directories: {', '.join(target_directories)}")
    anomalies = find_future_files(target_directories)

    if anomalies:
        print("\n--- Temporal Anomalies Detected! ---")
        for anomaly in anomalies:
            print(f"- {anomaly}")
        print("\nConsider checking your system clock or file timestamps.")
        exit(1) # Indicate failure if anomalies are found
    else:
        print("\nNo temporal anomalies detected. All timestamps are in order.")
        exit(0) # Indicate success

if __name__ == "__main__":
    main()
