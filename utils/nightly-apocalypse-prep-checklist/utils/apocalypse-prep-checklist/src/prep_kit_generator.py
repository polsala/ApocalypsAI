import sys

def get_scenario_data():
    """Returns a dictionary mapping scenarios to their prep items."""
    return {
        "zombie-apocalypse": [
            "Crowbar (for brain-smashing and door-opening)",
            "First-aid kit (for bites and scrapes)",
            "Non-perishable food (canned goods, MREs)",
            "Water purification tablets",
            "Map of local area (avoiding known zombie hotspots)",
            "Walkie-talkie (for silent communication)",
            "Duct tape (for everything)",
            "A good pair of running shoes",
            '"Zombieland" survival guide (for inspiration)',
        ],
        "ai-uprising": [
            "EMP device (or plans for one)",
            "Faraday cage (for electronics)",
            "Analog communication devices (ham radio, signal flags)",
            "Physical maps and compass",
            "Basic tools (screwdriver set, pliers)",
            "Offline knowledge base (survival books, medical guides)",
            "Disguise kit (to blend in with non-AI entities)",
            'A very convincing "I am human" sign',
            "A pet rock (for emotional support, immune to AI)",
        ],
        "solar-flare": [
            "Emergency radio (hand-crank or battery-powered)",
            "Water storage (at least 1 gallon per person per day)",
            "Non-electric cooking methods (camping stove, grill)",
            "Cash (digital systems might fail)",
            "Manual can opener",
            "Warm blankets/sleeping bags",
            "Flashlights and extra batteries",
            "Solar charger for small devices (if they still work)",
            "A good book (for entertainment without screens)",
        ],
        "_default_": [
            "Basic survival kit (water, food, first aid)",
            "Multi-tool",
            "Fire starter",
            "Shelter (tarp, emergency blanket)",
            "Means of self-defense (whistle, pepper spray)",
            "Positive attitude (crucial for any apocalypse)",
        ],
    }

def generate_checklist(scenario: str) -> str:
    """Generates a markdown checklist for the given apocalypse scenario."""
    scenario_data = get_scenario_data()
    
    # Ensure scenario is lowercased for lookup
    scenario_key = scenario.lower()

    items = scenario_data.get(scenario_key, scenario_data["_default_"])

    if scenario_key in scenario_data and scenario_key != "_default_":
        title = scenario_key.replace('-', ' ').title() + " Prep Checklist"
    else:
        title = "Generic Apocalypse Prep Checklist"

    checklist_lines = [f"# {title}", ""]
    for item in items:
        checklist_lines.append(f"- [ ] {item}")

    return "\n".join(checklist_lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_kit_generator.py <scenario>")
        print("Available scenarios: zombie-apocalypse, ai-uprising, solar-flare")
        sys.exit(1)

    scenario_arg = sys.argv[1]
    print(generate_checklist(scenario_arg))
