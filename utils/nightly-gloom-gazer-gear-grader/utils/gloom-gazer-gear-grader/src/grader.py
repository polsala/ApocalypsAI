import json
import argparse
import os
import sys

def load_json_file(filepath: str) -> dict | list:
    """Loads data from a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_default_rules() -> dict:
    """Returns the default grading rules."""
    return {
        "type_scores": {
            "weapon": 10,
            "tool": 8,
            "food": 7,
            "medicine": 12,
            "clothing": 5,
            "junk": -5
        },
        "condition_scores": {
            "new": 5,
            "used": 2,
            "damaged": -3,
            "broken": -10
        },
        "rarity_scores": {
            "rare": 10,
            "uncommon": 5,
            "common": 1,
            "legendary": 20
        },
        "weight_penalties": [
            {"threshold": 5, "penalty": -2},
            {"threshold": 10, "penalty": -5}
        ],
        "missing_attribute_penalty": -1
    }

def grade_item(item: dict, rules: dict) -> dict:
    """Calculates a survival score for a single item based on rules."""
    score = 0

    # Apply type scores
    item_type = item.get('type', '').lower()
    score += rules['type_scores'].get(item_type, rules['missing_attribute_penalty'])

    # Apply condition scores
    condition = item.get('condition', '').lower()
    score += rules['condition_scores'].get(condition, rules['missing_attribute_penalty'])

    # Apply rarity scores
    rarity = item.get('rarity', '').lower()
    score += rules['rarity_scores'].get(rarity, rules['missing_attribute_penalty'])

    # Apply weight penalties
    weight_kg = item.get('weight_kg', 0.0)
    for penalty_rule in rules['weight_penalties']:
        if weight_kg >= penalty_rule['threshold']:
            score += penalty_rule['penalty']

    return {**item, 'survival_score': score}

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-Gazer Gear Grader: Evaluate scavenged items."
    )
    parser.add_argument(
        '--items', 
        type=str, 
        required=True, 
        help="Path to the JSON file containing scavenged items."
    )
    parser.add_argument(
        '--rules', 
        type=str, 
        default=None, 
        help="Optional: Path to a custom JSON file with grading rules. Defaults to internal rules."
    )

    args = parser.parse_args()

    try:
        items_data = load_json_file(args.items)
        if not isinstance(items_data, list):
            raise ValueError("Items file must contain a JSON array of items.")

        if args.rules:
            grading_rules = load_json_file(args.rules)
        else:
            grading_rules = get_default_rules()

        graded_items = [grade_item(item, grading_rules) for item in items_data]
        graded_items.sort(key=lambda x: x['survival_score'], reverse=True)

        print(json.dumps(graded_items, indent=2))

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{args.items}' or '{args.rules}'.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
