import json
import sys
import os

SCENARIOS_FILE = os.path.join(os.path.dirname(__file__), 'scenarios.json')

def load_scenarios(file_path: str) -> dict:
    """Loads apocalypse scenarios from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Scenarios file not found at {file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}", file=sys.stderr)
        sys.exit(1)

def generate_checklist(scenario_name: str, scenarios_data: dict) -> str:
    """Generates a formatted checklist for a given scenario."""
    scenario = scenarios_data.get(scenario_name)
    if not scenario:
        return f"Error: Scenario '{scenario_name}' not found. Available scenarios: {', '.join(scenarios_data.keys())}"

    title = scenario.get('title', 'Untitled Scenario')
    description = scenario.get('description', 'No description provided.')
    items = scenario.get('items', [])

    checklist_output = f"# {title}\n\n"
    checklist_output += f"{description}\n\n"
    if items:
        checklist_output += "## Checklist:\n"
        for i, item in enumerate(items, 1):
            checklist_output += f"- [ ] {item}\n"
    else:
        checklist_output += "No items defined for this scenario.\n"

    return checklist_output

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/checklist_generator.py <scenario_name>", file=sys.stderr)
        sys.exit(1)

    scenario_name = sys.argv[1]
    scenarios = load_scenarios(SCENARIOS_FILE)

    if not scenarios:
        print("No scenarios loaded. Exiting.", file=sys.stderr)
        sys.exit(1)

    checklist = generate_checklist(scenario_name, scenarios)
    print(checklist)

if __name__ == '__main__':
    main()
