import argparse
import json
import os
import sys
import yaml

def find_config_files(root_path, extensions):
    """Recursively finds config files with specified extensions."""
    config_files = []
    if os.path.isfile(root_path):
        if any(root_path.lower().endswith(ext) for ext in extensions):
            config_files.append(root_path)
        return config_files

    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            if any(filename.lower().endswith(ext) for ext in extensions):
                config_files.append(os.path.join(dirpath, filename))
    return config_files

def process_file(filepath, indent, apply_changes):
    """
    Processes a single config file: validates and optionally normalizes.
    Returns (status, message, original_content, new_content)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return 'error', f"Failed to read file: {e}", None, None

    file_extension = os.path.splitext(filepath)[1].lower()
    parsed_data = None
    error_message = None
    new_content = original_content # Default to no change

    try:
        if file_extension in ('.yml', '.yaml'):
            parsed_data = yaml.safe_load(original_content)
            # yaml.safe_load returns None for empty files, which is valid.
            # If it's not None, we can try to dump it.
            if parsed_data is not None:
                new_content = yaml.dump(parsed_data, indent=indent, default_flow_style=False, sort_keys=False)
            else:
                new_content = original_content # Empty file, no change needed
        elif file_extension == '.json':
            parsed_data = json.loads(original_content)
            new_content = json.dumps(parsed_data, indent=indent, sort_keys=True)
        else:
            return 'skip', f"Unsupported file type: {file_extension}", original_content, original_content
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        error_message = f"Syntax error: {e}"
        return 'error', error_message, original_content, original_content
    except Exception as e:
        error_message = f"Unexpected error during parsing: {e}"
        return 'error', error_message, original_content, original_content

    # Compare stripped content to ignore differences only in leading/trailing whitespace, especially newlines
    if original_content.strip() != new_content.strip():
        if apply_changes:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return 'normalized', "File normalized successfully.", original_content, new_content
            except Exception as e:
                return 'error', f"Failed to write normalized file: {e}", original_content, new_content
        else:
            return 'needs_normalization', "File needs normalization.", original_content, new_content
    else:
        return 'ok', "File is already well-formed and formatted.", original_content, original_content

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Config Alchemist: Validate and normalize YAML/JSON config files."
    )
    parser.add_argument(
        '--path',
        required=True,
        help="The path to a file or directory to process. If a directory, it will be scanned recursively."
    )
    parser.add_argument(
        '--extensions',
        nargs='*',
        default=['.json', '.yml', '.yaml'],
        help="A space-separated list of file extensions to process (e.g., .json .yml)."
    )
    parser.add_argument(
        '--apply',
        action='store_true',
        help="If present, the utility will modify files to apply normalization. By default, it runs in 'check' mode."
    )
    parser.add_argument(
        '--indent',
        type=int,
        default=2,
        help="The number of spaces to use for indentation during normalization. Defaults to 2."
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    config_files = find_config_files(args.path, args.extensions)
    if not config_files:
        print(f"No config files found with extensions {args.extensions} in '{args.path}'.")
        sys.exit(0) # No-op

    print(f"\n--- Nightly Config Alchemist Report ({'Apply' if args.apply else 'Check'} Mode) ---")
    print(f"Scanning '{args.path}' for files with extensions: {', '.join(args.extensions)}\n")

    total_files = len(config_files)
    errors = 0
    needs_normalization = 0
    normalized_count = 0
    skipped_count = 0

    for filepath in config_files:
        status, message, _, _ = process_file(filepath, args.indent, args.apply)
        print(f"[{status.upper():<15}] {filepath}: {message}")
        if status == 'error':
            errors += 1
        elif status == 'needs_normalization':
            needs_normalization += 1
        elif status == 'normalized':
            normalized_count += 1
        elif status == 'skip':
            skipped_count += 1

    print(f"\n--- Summary ---")
    print(f"Total files processed: {total_files}")
    print(f"Files with errors: {errors}")
    print(f"Files needing normalization (check mode): {needs_normalization}")
    print(f"Files normalized (apply mode): {normalized_count}")
    print(f"Files skipped (unsupported type): {skipped_count}")
    print(f"Files already OK: {total_files - errors - needs_normalization - normalized_count - skipped_count}")

    if errors > 0:
        sys.exit(1) # Failure
    elif needs_normalization > 0:
        sys.exit(2) # No-op (needs changes, but not applied)
    else:
        sys.exit(0) # Success

if __name__ == '__main__':
    main()
