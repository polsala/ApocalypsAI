import random
import os

def get_resources(filepath="resources.txt"):
    """Reads resources from the specified file."""
    script_dir = os.path.dirname(__file__)
    abs_filepath = os.path.join(script_dir, filepath)
    try:
        with open(abs_filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        # Fallback for robustness, though resources.txt should always be present
        return ["Dusty Data-chips", "Forgotten Firmware", "Empty Promises"]

def scavenge():
    """Simulates scavenging for resources and reports findings."""
    available_resources = get_resources()
    if not available_resources:
        print("Scavenger Bot reports: The wasteland is barren today. No resources found.")
        return

    # Randomly decide how many resources to find (0 to 3)
    num_found = random.randint(0, min(3, len(available_resources)))

    if num_found == 0:
        print("Scavenger Bot reports: A thorough search yielded nothing but echoes of the past.")
    else:
        # Randomly select unique items from the available resources
        found_items = random.sample(available_resources, num_found)
        print(f"Scavenger Bot reports: Found {num_found} valuable items!")
        for item in found_items:
            print(f"- {item}")

if __name__ == "__main__":
    scavenge()
