import argparse
import json
import os
import yaml

def clean_data(data, keys_to_remove=None):
    """
    Recursively cleans a data structure (dict or list) by:
    - Removing empty dictionaries {}
    - Removing empty lists []
    - Removing None/null values
    - Removing specified keys
    """
    if keys_to_remove is None:
        keys_to_remove = set()
    else:
        keys_to_remove = set(keys_to_remove)

    if isinstance(data, dict):
        cleaned_dict = {}
        for k, v in data.items():
            if k in keys_to_remove:
                continue # Skip this key entirely
            cleaned_v = clean_data(v, keys_to_remove)
            if cleaned_v is not None and cleaned_v != {} and cleaned_v != []:
                cleaned_dict[k] = cleaned_v
        return cleaned_dict if cleaned_dict else None # Return None if dict becomes empty
    elif isinstance(data, list):
        cleaned_list = []
        for item in data:
            cleaned_item = clean_data(item, keys_to_remove)
            if cleaned_item is not None and cleaned_item != {} and cleaned_item != []:
                cleaned_list.append(cleaned_item)
        return cleaned_list if cleaned_list else None # Return None if list becomes empty
    else:
        return data if data is not None else None

def main():
    parser = argparse.ArgumentParser(
        description="Clean up messy JSON or YAML files by removing empty objects, arrays, nulls, and specified keys."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the input JSON or YAML file."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path where the cleaned output file will be saved."
    )
    parser.add_argument(
        "--remove-keys",
        nargs='*',
        default=[],
        help="Space-separated list of keys to remove from the data."
    )

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    keys_to_remove = args.remove_keys

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at '{input_path}'")
        exit(1)

    _, input_ext = os.path.splitext(input_path)
    input_ext = input_ext.lower()

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            if input_ext == '.json':
                data = json.load(f)
            elif input_ext in ('.yaml', '.yml'):
                data = yaml.safe_load(f)
            else:
                print(f"Error: Unsupported input file type '{input_ext}'. Only .json, .yaml, .yml are supported.")
                exit(1)
    except (json.JSONDecodeError, yaml.YAMLError) as e:
        print(f"Error parsing input file '{input_path}': {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading input file: {e}")
        exit(1)

    cleaned_data = clean_data(data, keys_to_remove)

    _, output_ext = os.path.splitext(output_path)
    output_ext = output_ext.lower()

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            if output_ext == '.json':
                json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
            elif output_ext in ('.yaml', '.yml'):
                yaml.safe_dump(cleaned_data, f, indent=2, allow_unicode=True)
            else:
                print(f"Error: Unsupported output file type '{output_ext}'. Only .json, .yaml, .yml are supported.")
                exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while writing output file: {e}")
        exit(1)

    print(f"Successfully scrubbed '{input_path}' and saved to '{output_path}'.")

if __name__ == "__main__":
    main()
