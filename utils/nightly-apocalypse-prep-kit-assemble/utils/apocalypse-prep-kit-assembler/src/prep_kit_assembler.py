import argparse
import subprocess
import os
import sys

def assemble_prep_kit(requirements_file: str, output_dir: str) -> None:
    """
    Downloads all packages from a requirements file into a specified output directory
    for offline installation.
    """
    if not os.path.exists(requirements_file):
        print(f"Error: Requirements file not found at '{requirements_file}'", file=sys.stderr)
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)

    print(f"Assembling apocalypse prep kit for '{requirements_file}' into '{output_dir}'...")
    try:
        # Use pip download to get all packages and their dependencies
        # --dest or -d specifies the download directory
        # --requirement or -r specifies the requirements file
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'download', '-r', requirements_file, '-d', output_dir],
            check=True,  # Raise CalledProcessError for non-zero exit codes
            capture_output=True, # Capture stdout and stderr
            text=True # Decode stdout/stderr as text
        )
        print("\n--- pip download stdout ---")
        print(result.stdout)
        print("\n--- pip download stderr ---")
        print(result.stderr)
        print(f"Successfully assembled prep kit in '{output_dir}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error assembling prep kit: pip command failed with exit code {e.returncode}", file=sys.stderr)
        print(f"Command: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"Stdout:\n{e.stdout}", file=sys.stderr)
        print(f"Stderr:\n{e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'pip' command not found. Ensure Python and pip are installed and in your PATH.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Assemble an apocalypse prep kit by downloading Python dependencies for offline installation."
    )
    parser.add_argument(
        '--requirements', 
        type=str, 
        required=True, 
        help='Path to the requirements.txt file.'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        required=True, 
        help='Path to the directory where downloaded packages will be stored.'
    )

    args = parser.parse_args()
    assemble_prep_kit(args.requirements, args.output)
