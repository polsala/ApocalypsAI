import argparse
import yaml
import json
import sys
from typing import Dict, Any, List, Tuple

def calculate_depletion(current_amount: float, daily_consumption: float) -> float:
    """Calculates days until depletion."""
    if daily_consumption <= 0:
        return float('inf') # Infinite days if no consumption or negative consumption
    return current_amount / daily_consumption

def get_status_emoji(days_left: float) -> Tuple[str, str]:
    """Returns a status emoji and description based on days left."""
    if days_left == float('inf'):
        return "🟢", "Plenty"
    elif days_left > 30:
        return "🟢", "Plenty"
    elif days_left >= 15:
        return "🟡", "Stable"
    elif days_left >= 5:
        return "🟠", "Warning"
    elif days_left >= 1:
        return "🔴", "Critical"
    else:
        return "💀", "Depleted"

def load_config(config_path: str) -> Dict[str, Any]:
    """Loads configuration from a YAML or JSON file."""
    try:
        with open(config_path, 'r') as f:
            if config_path.endswith(('.yaml', '.yml')):
                return yaml.safe_load(f)
            elif config_path.endswith('.json'):
                return json.load(f)
            else:
                print(f"Error: Unsupported config file format for {config_path}. Use .yaml, .yml, or .json.", file=sys.stderr)
                sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Config file not found at {config_path}", file=sys.stderr)
        sys.exit(1)
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        print(f"Error: Failed to parse config file {config_path}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Forecast resource depletion based on current stock and daily consumption."
    )
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the YAML or JSON configuration file for resources."
    )

    args = parser.parse_args()
    config = load_config(args.config)

    resources: List[Dict[str, Any]] = config.get('resources', [])
    if not resources:
        print("No resources defined in the configuration file.", file=sys.stderr)
        sys.exit(0)

    # Print header
    print(f"{'Resource':<25} | {'Current':<7} | {'Consump.':<8} | {'Days Left':<9} | {'Status':<15}")
    print(f"{'-'*25}-+-{'-'*7}-+-{'-'*8}-+-{'-'*9}-+-{'-'*15}")

    for resource in resources:
        name = resource.get('name', 'Unknown Resource')
        current_amount = float(resource.get('current_amount', 0))
        daily_consumption = float(resource.get('daily_consumption', 0))

        days_left = calculate_depletion(current_amount, daily_consumption)
        emoji, status_desc = get_status_emoji(days_left)

        days_left_str = f"{days_left:.1f}" if days_left != float('inf') else "∞"

        print(
            f"{name:<25} | {current_amount:<7.1f} | {daily_consumption:<8.1f} | {days_left_str:<9} | {emoji} {status_desc}"
        )

if __name__ == "__main__":
    main()
