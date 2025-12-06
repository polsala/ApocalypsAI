import json
import os

class ChecklistGenerator:
    def __init__(self, scenarios_file='scenarios.json'):
        self.scenarios_file = os.path.join(os.path.dirname(__file__), scenarios_file)
        self.data = self._load_scenarios()

    def _load_scenarios(self):
        # Mock rationale: In a real scenario, this would load from a file.
        # For testing, we might want to inject a mock file content or path.
        try:
            with open(self.scenarios_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Scenarios file not found at {self.scenarios_file}")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.scenarios_file}")
            return None

    def get_available_scenarios(self):
        if not self.data:
            return []
        return list(self.data['scenarios'].keys())

    def generate_checklist(self, selected_scenario_keys, user_resources):
        if not self.data:
            return "Error: Scenarios data not loaded."

        output = []
        user_resources_lower = {res.strip().lower() for res in user_resources}

        # Sort scenarios by name for deterministic output
        sorted_scenario_keys = sorted(selected_scenario_keys, key=lambda k: self.data['scenarios'][k]['name'])

        for key in sorted_scenario_keys:
            scenario = self.data['scenarios'].get(key)
            if not scenario:
                output.append(f"Warning: Scenario '{key}' not found.\n")
                continue

            output.append(f"\nScenario: {scenario['name']}")
            output.append(f"Description: {scenario['description']}\n")

            all_items = set(self.data['general_items'] + scenario['specific_items'])
            
            for item in sorted(list(all_items)):
                status = "[HAVE]" if item.lower() in user_resources_lower else "[ ]"
                output.append(f"{status} {item}")
            
            output.append(f"\nWhimsical Advice: {scenario['whimsical_advice']}\n")

        return "\n".join(output)

def main():
    print("Welcome, future survivor! Let's prepare for the end...\n")
    generator = ChecklistGenerator()

    if not generator.data:
        print("Exiting due to data loading error.")
        return

    available_scenarios = generator.get_available_scenarios()
    if not available_scenarios:
        print("No scenarios available. Exiting.")
        return

    print("Select apocalypse scenarios (comma-separated, e.g., '1,3'):")
    for i, key in enumerate(available_scenarios):
        print(f"{i+1}. {generator.data['scenarios'][key]['name']}")

    selected_scenario_keys = []
    while not selected_scenario_keys:
        try:
            choice_str = input("Your choice: ").strip()
            choices = [int(c.strip()) for c in choice_str.split(',') if c.strip()]
            
            temp_selected_keys = []
            for c in choices:
                if 1 <= c <= len(available_scenarios):
                    temp_selected_keys.append(available_scenarios[c-1])
                else:
                    print(f"Invalid choice: {c}. Please enter numbers between 1 and {len(available_scenarios)}.")
            
            if temp_selected_keys:
                selected_scenario_keys = list(set(temp_selected_keys)) # Remove duplicates
            else:
                print("No valid scenarios selected. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")

    user_resources_input = input("\nEnter items you already have (comma-separated, e.g., 'Water filter,First aid kit'): ").strip()
    user_resources = [res.strip() for res in user_resources_input.split(',') if res.strip()]

    print("\n--- Your Personalized Apocalypse Prep Checklist ---")
    print(generator.generate_checklist(selected_scenario_keys, user_resources))
    print("--------------------------------------------------")
    print("Good luck, survivor! May your preps be plentiful and your doom be delayed.")

if __name__ == '__main__':
    main()
