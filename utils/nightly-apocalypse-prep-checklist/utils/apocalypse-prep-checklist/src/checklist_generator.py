def generate_checklist(scenario_input: str) -> str:
    """
    Generates a whimsical-yet-useful apocalypse preparedness checklist
    for a given scenario.
    """
    original_scenario_name = scenario_input # Keep original for title
    normalized_input = scenario_input.lower().replace(' ', '_')

    general_items = [
        "Water (1 gallon per person per day, 3-day supply minimum)",
        "Non-perishable food (3-day supply minimum)",
        "First aid kit (with extra meds)",
        "Flashlight and extra batteries",
        "Whistle (to signal for help)",
        "Dust mask (to filter contaminated air)",
        "Wrench or pliers (to turn off utilities)",
        "Manual can opener",
        "Local maps (physical, not digital)",
        "Battery-powered or hand-crank radio",
        "Chargers and power bank for cell phones",
        "Cash (small bills)",
        "Important documents (copies in waterproof bag)",
        "Sleeping bag or warm blanket for each person",
        "Fire extinguisher",
        "Matches or lighter",
        "Multi-tool",
        "Personal hygiene items",
        "Pet food and extra water for pets",
        "Books, games, puzzles (for entertainment)",
        "Duct tape (the ultimate survival tool)",
        "Plastic sheeting (to create a shelter-in-place seal)",
    ]

    scenario_specific_items = {
        "zombie": [
            "Crowbar or blunt weapon (for 'persuasion')",
            "Running shoes (for quick escapes)",
            "Bite-proof clothing (if you can find it)",
            "Decoy noisemakers (to distract the 'unliving')",
            "A copy of 'The Zombie Survival Guide'",
        ],
        "meteor": [
            "Hard hat or helmet (for falling debris)",
            "Sturdy underground shelter plans",
            "Radiation counter (just in case)",
            "Emergency beacon (for post-impact rescue)",
            "Telescope (to watch the show... from a safe distance)",
        ],
        "ai_uprising": [
            "EMP-proof Faraday cage (for electronics)",
            "Analog communication devices (walkie-talkies)",
            "Offline maps and navigation tools",
            "A good old-fashioned axe (for 'rebooting' rogue servers')",
            "Disguise kit (to blend in with the 'unaugmented')",
        ],
        "general": [],
    }

    items = list(general_items)
    warning_message = ""
    active_scenario_key = None

    # Determine the active scenario key based on normalized input
    for key in scenario_specific_items.keys():
        if key != "general" and key in normalized_input:
            active_scenario_key = key
            break
    
    if active_scenario_key:
        items.extend(scenario_specific_items[active_scenario_key])
    else:
        # If no specific scenario found, and it's not explicitly 'general', issue a warning.
        if normalized_input != "general":
            warning_message = f"**Warning**: Unknown or unsupported specific scenario '{original_scenario_name}'. Generating a general preparedness checklist.\n\n"

    checklist_title = f"# Apocalypse Preparedness Checklist: {original_scenario_name.replace('_', ' ').title()}"
    checklist_items = "\n".join([f"- [ ] {item}" for item in items])

    return f"{checklist_title}\n\n{warning_message}{checklist_items}\n"

if __name__ == "__main__":
    print("--- Zombie Apocalypse Checklist ---")
    print(generate_checklist("zombie"))
    print("\n--- Meteor Impact Checklist ---")
    print(generate_checklist("meteor"))
    print("\n--- AI Uprising Checklist ---")
    print(generate_checklist("ai_uprising"))
    print("\n--- General Preparedness Checklist ---")
    print(generate_checklist("general"))
    print("\n--- Unknown Scenario Checklist (Alien Invasion) ---")
    print(generate_checklist("alien_invasion"))
    print("\n--- Scenario with spaces (Zombie Apocalypse) ---")
    print(generate_checklist("zombie apocalypse"))
    print("\n--- Scenario with spaces (AI Robot Uprising) ---")
    print(generate_checklist("AI Robot Uprising"))
