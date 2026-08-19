import sys
import os

def get_suggestions(item):
    item_lower = item.lower().strip()
    mappings = {
        "water filter": {"function": "Hydration Management", "tool": "apocalypsai/aqua-purifier-bot:latest"},
        "first aid kit": {"function": "Emergency Medicine", "tool": "apocalypsai/med-scanner-cli:latest"},
        "radio": {"function": "Long-Range Comms", "tool": "apocalypsai/signal-scout-cli:latest"},
        "seeds": {"function": "Sustainable Agriculture", "tool": "apocalypsai/terra-cultivator-ai:latest"},
        "flashlight": {"function": "Illumination & Power", "tool": "apocalypsai/lumina-charger-sim:latest"},
        "knife": {"function": "Utility & Defense", "tool": "apocalypsai/blade-sharpener-bot:latest"},
        "map": {"function": "Navigation & Cartography", "tool": "apocalypsai/wayfinder-atlas-cli:latest"},
        "compass": {"function": "Directional Guidance", "tool": "apocalypsai/true-north-oracle:latest"},
        "fire starter": {"function": "Heat & Cooking", "tool": "apocalypsai/pyro-igniter-assist:latest"},
        "rope": {"function": "Utility & Securing", "tool": "apocalypsai/knot-tying-master:latest"},
        "canned food": {"function": "Ration Management", "tool": "apocalypsai/ration-rotator-cli:latest"},
        "books": {"function": "Knowledge Preservation", "tool": "apocalypsai/lore-keeper-archive:latest"},
        "meds": {"function": "Pharmaceutical Supply", "tool": "apocalypsai/pharma-tracker-cli:latest"},
        "solar panel": {"function": "Renewable Energy", "tool": "apocalypsai/sun-harvest-monitor:latest"},
        "axe": {"function": "Resource Gathering", "tool": "apocalypsai/wood-chopper-bot:latest"},
        "tent": {"function": "Shelter & Protection", "tool": "apocalypsai/shelter-builder-ai:latest"},
        "sleeping bag": {"function": "Comfort & Rest", "tool": "apocalypsai/rest-optimizer-cli:latest"},
        "cooking pot": {"function": "Food Preparation", "tool": "apocalypsai/chef-bot-assistant:latest"},
        "fishing kit": {"function": "Food Acquisition", "tool": "apocalypsai/angler-assist-ai:latest"},
        "gardening tools": {"function": "Crop Cultivation", "tool": "apocalypsai/agri-drone-planner:latest"},
        "duct tape": {"function": "Repair & Improvise", "tool": "apocalypsai/fixit-bot-guide:latest"},
        "multi-tool": {"function": "Versatile Utility", "tool": "apocalypsai/swiss-army-ai:latest"}
    }
    return mappings.get(item_lower, {"function": "General Survival", "tool": "apocalypsai/generic-survival-aid:latest"})

def main():
    if len(sys.argv) < 2:
        print("Usage: python survival_kit_dockerizer.py <path_to_kit_file>")
        sys.exit(1)

    kit_file_path = sys.argv[1]

    if not os.path.exists(kit_file_path):
        print(f"Error: Kit file not found at '{kit_file_path}'", file=sys.stderr)
        sys.exit(1)

    print("Processing survival kit...\n")
    try:
        with open(kit_file_path, 'r') as f:
            for line in f:
                item = line.strip()
                if item:
                    suggestions = get_suggestions(item)
                    print(f"Item: {item}")
                    print(f"  Survival Function: {suggestions['function']}")
                    print(f"  Suggested Docker Tool: {suggestions['tool']}\n")
    except Exception as e:
        print(f"An error occurred while reading the kit file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
