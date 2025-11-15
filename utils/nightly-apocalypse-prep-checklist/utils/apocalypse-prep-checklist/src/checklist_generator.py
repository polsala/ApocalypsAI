import json
import os

def load_scenarios(data_path):
    """Loads scenarios and general items from a JSON file."""
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {data_path}")
        return None

def get_scenario_choice(scenarios):
    """Prompts user to choose a scenario."""
    print("\nAvailable Apocalypse Scenarios:")
    for i, scenario in enumerate(scenarios):
        print(f"  {i+1}. {scenario['name']} ({', '.join(scenario['keywords'])})")

    while True:
        try:
            choice = input("Enter the number of your chosen scenario: ").strip()
            scenario_index = int(choice) - 1
            if 0 <= scenario_index < len(scenarios):
                return scenarios[scenario_index]
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_location_choice():
    """Prompts user to choose a location type."""
    while True:
        location = input("Are you in an (urban) or (rural) area? ").strip().lower()
        if location in ['urban', 'rural']:
            return location
        else:
            print("Invalid location. Please enter 'urban' or 'rural'.")

def get_people_count():
    """Prompts user for the number of people in their group."""
    while True:
        try:
            count = int(input("How many people are in your survival group? ").strip())
            if count > 0:
                return count
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def generate_checklist(
    scenario_data,
    chosen_scenario,
    location_type,
    people_count
):
    """Generates a personalized checklist, categorized."""
    categorized_checklist = {
        "General Essentials": [],
        "Scenario-Specific": [],
        "Location-Specific": [],
        "Group-Specific": []
    }

    # Add general items
    if scenario_data.get('general_items'):
        categorized_checklist["General Essentials"].extend(scenario_data['general_items'])

    # Add base scenario items
    if chosen_scenario.get('base_items'):
        categorized_checklist["Scenario-Specific"].extend(chosen_scenario['base_items'])

    # Add location-specific items
    if location_type in chosen_scenario.get('location_specific', {}):
        categorized_checklist["Location-Specific"].extend(chosen_scenario['location_specific'][location_type])

    # Add people-specific items
    people_specific_items = chosen_scenario.get('people_specific', {})
    if people_count == 1 and '1' in people_specific_items:
        categorized_checklist["Group-Specific"].extend(people_specific_items['1'])
    elif 2 <= people_count <= 5 and '2-5' in people_specific_items:
        categorized_checklist["Group-Specific"].extend(people_specific_items['2-5'])
    elif people_count >= 6 and '6+' in people_specific_items:
        categorized_checklist["Group-Specific"].extend(people_specific_items['6+'])

    # Remove duplicates and sort within each category
    for category in categorized_checklist:
        categorized_checklist[category] = sorted(list(set(categorized_checklist[category])))

    return categorized_checklist

def display_checklist(
    scenario_name,
    location_type,
    people_count,
    categorized_checklist
):
    """Prints the generated checklist to the console, categorized."""
    print(f"\n--- Your Apocalypse Preparedness Checklist ({scenario_name}, {location_type.capitalize()}, {people_count} People) ---")

    for category, items in categorized_checklist.items():
        if items: # Only print categories that have items
            print(f"\n{category}:")
            for item in items:
                print(f"- {item}")
    print("\n--------------------------------------------------------------------------------")


if __name__ == "__main__":
    # Determine the path to the data file relative to the script's location
    script_dir = os.path.dirname(__file__)
    data_file_path = os.path.join(script_dir, '..', 'data', 'scenarios.json')

    scenario_data = load_scenarios(data_file_path)

    if scenario_data and scenario_data.get('scenarios'):
        chosen_scenario = get_scenario_choice(scenario_data['scenarios'])
        if chosen_scenario:
            location_type = get_location_choice()
            people_count = get_people_count()

            final_checklist = generate_checklist(
                scenario_data,
                chosen_scenario,
                location_type,
                people_count
            )
            display_checklist(
                chosen_scenario['name'],
                location_type,
                people_count,
                final_checklist
            )
    else:
        print("Could not load scenario data. Exiting.")
