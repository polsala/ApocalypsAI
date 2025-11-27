import hashlib
import json
import os
import sys
from datetime import datetime

def calculate_file_checksum(filepath, algorithm='sha256'):
    """Calculates the checksum of a single file."""
    hasher = hashlib.md5() if algorithm == 'md5' else hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def calculate_directory_checksums(directory, algorithm='sha256'):
    """
    Calculates checksums for all files in a given directory and its subdirectories.
    Returns a dictionary where keys are relative file paths and values are checksums.
    """
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    checksums = {}
    base_path = os.path.abspath(directory)

    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, base_path)
            checksums[relative_path] = calculate_file_checksum(filepath, algorithm)
    return checksums

def save_manifest(manifest_data, output_path):
    """Saves the manifest data to a JSON file."""
    with open(output_path, 'w') as f:
        json.dump(manifest_data, f, indent=4)

def load_manifest(input_path):
    """Loads a manifest from a JSON file."""
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Manifest file not found: {input_path}")
    with open(input_path, 'r') as f:
        return json.load(f)

def generate_manifest_cli(args):
    """CLI handler for generating a manifest."""
    if len(args) < 2:
        print("Usage: generate <directory_to_scan> <output_manifest_path> [--algorithm <md5|sha256>]")
        sys.exit(1)

    directory = args[0]
    output_path = args[1]
    algorithm = 'sha256'
    if '--algorithm' in args:
        try:
            algo_index = args.index('--algorithm') + 1
            if algo_index < len(args):
                chosen_algo = args[algo_index].lower()
                if chosen_algo in ['md5', 'sha256']:
                    algorithm = chosen_algo
                else:
                    print(f"Error: Invalid algorithm '{chosen_algo}'. Choose 'md5' or 'sha256'.")
                    sys.exit(1)
            else:
                print("Error: --algorithm requires a value (md5 or sha256).")
                sys.exit(1)
        except ValueError:
            pass # Should not happen if '--algorithm' is in args

    try:
        print(f"Scanning directory '{directory}' using {algorithm.upper()}...")
        checksums = calculate_directory_checksums(directory, algorithm)
        manifest_data = {
            "generated_at": datetime.now().isoformat(),
            "algorithm": algorithm,
            "checksums": checksums
        }
        save_manifest(manifest_data, output_path)
        print(f"Manifest saved to '{output_path}' with {len(checksums)} files.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def verify_manifest_cli(args):
    """CLI handler for verifying a manifest."""
    if len(args) < 2:
        print("Usage: verify <directory_to_verify> <input_manifest_path> [--algorithm <md5|sha256>]")
        sys.exit(1)

    directory = args[0]
    input_path = args[1]
    algorithm_override = None
    if '--algorithm' in args:
        try:
            algo_index = args.index('--algorithm') + 1
            if algo_index < len(args):
                chosen_algo = args[algo_index].lower()
                if chosen_algo in ['md5', 'sha256']:
                    algorithm_override = chosen_algo
                else:
                    print(f"Error: Invalid algorithm '{chosen_algo}'. Choose 'md5' or 'sha256'.")
                    sys.exit(1)
            else:
                print("Error: --algorithm requires a value (md5 or sha256).")
                sys.exit(1)
        except ValueError:
            pass

    try:
        print(f"Loading manifest from '{input_path}'...")
        manifest = load_manifest(input_path)
        manifest_checksums = manifest.get("checksums", {})
        manifest_algorithm = manifest.get("algorithm", "sha256")

        if algorithm_override and algorithm_override != manifest_algorithm:
            print(f"Warning: Manifest was generated with '{manifest_algorithm}', but verification requested with '{algorithm_override}'. Using manifest's algorithm for verification.")
        
        current_checksums = calculate_directory_checksums(directory, manifest_algorithm)

        print(f"Verifying directory '{directory}' against manifest using {manifest_algorithm.upper()}...")

        matched_files = []
        mismatched_files = []
        new_files = []
        missing_files = []

        # Check for mismatches and matches
        for rel_path, manifest_checksum in manifest_checksums.items():
            if rel_path in current_checksums:
                if current_checksums[rel_path] == manifest_checksum:
                    matched_files.append(rel_path)
                else:
                    mismatched_files.append(rel_path)
            else:
                missing_files.append(rel_path)

        # Check for new files
        for rel_path in current_checksums:
            if rel_path not in manifest_checksums:
                new_files.append(rel_path)

        print("\n--- Verification Report ---")
        if matched_files:
            print(f"\n✅ {len(matched_files)} files matched checksums:")
            for f in matched_files:
                print(f"  - {f}")
        if mismatched_files:
            print(f"\n❌ {len(mismatched_files)} files had mismatched checksums (modified):")
            for f in mismatched_files:
                print(f"  - {f}")
        if new_files:
            print(f"\n➕ {len(new_files)} new files found (not in manifest):")
            for f in new_files:
                print(f"  - {f}")
        if missing_files:
            print(f"\n➖ {len(missing_files)} files missing (in manifest but not in directory):")
            for f in missing_files:
                print(f"  - {f}")

        if not mismatched_files and not new_files and not missing_files:
            print("\n✨ All files verified successfully! No changes detected.")
        else:
            print("\n⚠️ Verification completed with discrepancies.")
            sys.exit(1) # Indicate failure if discrepancies exist

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in manifest file '{input_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/checksum_keeper.py <command> [args...]")
        print("Commands:")
        print("  generate <directory> <output_manifest_path> [--algorithm <md5|sha256>]")
        print("  verify <directory> <input_manifest_path> [--algorithm <md5|sha256>]")
        sys.exit(1)

    command = sys.argv[1]
    command_args = sys.argv[2:]

    if command == "generate":
        generate_manifest_cli(command_args)
    elif command == "verify":
        verify_manifest_cli(command_args)
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
