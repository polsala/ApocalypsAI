import argparse
import datetime
from collections import defaultdict

def parse_item_line(line: str) -> dict:
    """Parses a single line from the input file into an item dictionary."""
    parts = [p.strip() for p in line.split('|')]
    if len(parts) < 2:
        return None # Invalid line

    item_name = parts[0]
    category = parts[1]
    tags = [t.strip() for t in parts[2].split(',') if t.strip()] if len(parts) > 2 else []

    return {
        'name': item_name,
        'category': category,
        'tags': tags
    }

def generate_markdown_manifest(items: list[dict]) -> str:
    """Generates a Markdown string from a list of parsed items."""
    manifest_date = datetime.date.today().strftime('%Y-%m-%d')
    output_lines = [f"# Scavenger's Manifest - {manifest_date}", ""]

    categorized_items = defaultdict(list)
    for item in items:
        categorized_items[item['category']].append(item)

    # Sort categories alphabetically
    sorted_categories = sorted(categorized_items.keys())

    for category in sorted_categories:
        output_lines.append(f"## {category}")
        # Sort items within each category alphabetically by name
        for item in sorted(categorized_items[category], key=lambda x: x['name']):
            tags_str = f" ({', '.join(item['tags'])})" if item['tags'] else ""
            output_lines.append(f"- {item['name']}{tags_str}")
        output_lines.append("") # Add a blank line after each category

    return "\n".join(output_lines).strip()

def main():
    parser = argparse.ArgumentParser(
        description="Generate a categorized Markdown manifest from scavenged items."
    )
    parser.add_argument(
        '-i', '--input', 
        type=str, 
        required=True, 
        help="Path to the input text file with scavenged items."
    )
    parser.add_argument(
        '-o', '--output', 
        type=str, 
        required=True, 
        help="Path to the output Markdown manifest file."
    )

    args = parser.parse_args()

    parsed_items = []
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'): # Ignore empty lines and comments
                    item = parse_item_line(line)
                    if item:
                        parsed_items.append(item)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    if not parsed_items:
        print("No valid items found in the input file. Generating empty manifest.")

    markdown_output = generate_markdown_manifest(parsed_items)

    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        print(f"Manifest successfully generated at '{args.output}'.")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == '__main__':
    main()
