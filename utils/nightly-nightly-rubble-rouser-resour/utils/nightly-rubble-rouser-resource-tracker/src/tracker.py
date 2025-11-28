import argparse
import os
from typing import Dict, List

def load_resources(file_path: str) -> Dict[str, int]:
    """
    Loads resources from a plain text file.
    Each line should be in the format "Resource Name: Quantity".
    """
    resources: Dict[str, int] = {}
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resource file not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            try:
                name, quantity_str = line.split(':', 1)
                quantity = int(quantity_str.strip())
                if quantity < 0:
                    print(f"Warning: Negative quantity for '{name}'. Skipping.")
                    continue
                resources[name.strip()] = quantity
            except ValueError:
                print(f"Warning: Could not parse line '{line}'. Skipping.")
    return resources

def summarize_resources(resources: Dict[str, int]) -> List[str]:
    """
    Generates a summary of all resources.
    """
    summary_lines = ["--- Resource Inventory Summary ---"]
    if not resources:
        summary_lines.append("No resources tracked.")
        return summary_lines

    for name, quantity in sorted(resources.items()):
        summary_lines.append(f"{name}: {quantity} units")
    return summary_lines

def identify_low_resources(resources: Dict[str, int], threshold: int) -> List[str]:
    """
    Identifies resources with quantities below the given threshold.
    """
    low_resources_lines = [f"--- Low Resources (below {threshold} units) ---"]
    found_low = False
    for name, quantity in sorted(resources.items()):
        if quantity < threshold:
            low_resources_lines.append(f"{name}: {quantity} units (CRITICAL!)")
            found_low = True
    
    if not found_low:
        low_resources_lines.append("All resources are above the threshold. Good job!")
    return low_resources_lines

def main():
    parser = argparse.ArgumentParser(
        description="Track scavenged resources and identify low stock."
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to the resource inventory file (e.g., resources.txt)"
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=10,
        help="Quantity below which a resource is considered 'low' (default: 10)"
    )

    args = parser.parse_args()

    try:
        resources = load_resources(args.file)
        
        print("\n".join(summarize_resources(resources)))
        print("\n")
        print("\n".join(identify_low_resources(resources, args.threshold)))

    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
