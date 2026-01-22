import re
import sys
import argparse

def scrub_data(input_path, output_path):
    """Reads raw data, extracts specific patterns, and writes to a CSV file."""
    extracted_data = []
    resource_pattern = re.compile(r"\[RESOURCE:([^\]]+)\]")
    amount_pattern = re.compile(r"Amount:\s*(\d+)\s*units?")
    location_pattern = re.compile(r"Location:\s*\(COORD:([-\d.]+),([-\d.]+)\)")

    try:
        with open(input_path, 'r') as infile:
            for line in infile:
                if "DATA:" in line: # Only process lines explicitly marked as data
                    resource_match = resource_pattern.search(line)
                    amount_match = amount_pattern.search(line)
                    location_match = location_pattern.search(line)

                    resource = resource_match.group(1) if resource_match else "UNKNOWN"
                    amount = amount_match.group(1) if amount_match else "N/A"
                    location = f"{location_match.group(1)},{location_match.group(2)}" if location_match else "N/A"

                    extracted_data.append(f"{resource},{amount},{location}")
        
        with open(output_path, 'w') as outfile:
            outfile.write("Resource,Amount,Location\n") # Write CSV header
            for item in extracted_data:
                outfile.write(item + "\n")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during scrubbing: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Wasteland Data Scrubber: Extracts vital information from raw logs."
    )
    parser.add_argument("--input", required=True, help="Path to the raw input data file.")
    parser.add_argument("--output", required=True, help="Path to the cleaned output CSV file.")
    args = parser.parse_args()

    scrub_data(args.input, args.output)
