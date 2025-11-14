import argparse
import textwrap

def get_base_checklist():
    """Returns a foundational list of preparedness items."""
    return [
        "Water (1 gallon per person per day for at least 3 days)",
        "Non-perishable food (3-day supply)",
        "First aid kit",
        "Whistle (to signal for help)",
        "Dust mask (to filter contaminated air)",
        "Plastic sheeting and duct tape (to shelter-in-place)",
        "Moist towelettes, garbage bags, and plastic ties (for sanitation)",
        "Wrench or pliers (to turn off utilities)",
        "Manual can opener (for food)",
        "Local maps",
        "Battery-powered or hand-crank radio and a NOAA Weather Radio with tone alert",
        "Flashlight and extra batteries",
        "Cell phone with chargers and a backup battery",
        "Cash (small bills)",
        "Important documents (copies in waterproof bag)",
        "Prescription medications and glasses",
        "Infant formula and diapers (if applicable)",
        "Pet food and extra water for your pet (if applicable)",
        "Sleeping bag or warm blanket for each person",
        "Change of clothing for each person",
        "Fire extinguisher",
        "Matches in a waterproof container",
        "Personal hygiene items",
        "Books, games, puzzles, or other activities for children",
    ]

def get_scenario_specific_items(scenario):
    """Returns items specific to a given apocalypse scenario."""
    scenario_items = {
        "zombie": [
            "Crowbar or blunt weapon (for close encounters)",
            "Machete or sharp blade (for clearing paths)",
            "Durable clothing (bite protection)",
            "Quiet footwear",
            "Knowledge of zombie weak points (headshots!)",
            "Emergency brain-repellent spray (experimental)",
        ],
        "nuclear": [
            "Potassium iodide pills (radiation protection)",
            "Geiger counter (radiation detection)",
            "Lead-lined bunker plans",
            "Heavy-duty hazmat suit",
            "Water purification tablets (for fallout-contaminated water)",
            "Long-term food storage (canned goods, MREs)",
        ],
        "ai_uprising": [
            "EMP device (theoretical, for disabling electronics)",
            "Faraday cage (for protecting electronics)",
            "Analog communication devices (walkie-talkies, signal flares)",
            "Manuals for pre-digital technology",
            "Disguise kit (to avoid facial recognition)",
            "Offline maps and navigation tools",
        ],
        "alien_invasion": [
            "Universal translator (if you're lucky)",
            "Laser pointer (for distracting alien overlords)",
            "Tin foil hat (for mind-control resistance)",
            "Advanced alien weaponry schematics (if you can find them)",
            "Camouflage gear (to blend with local flora/fauna)",
            "Emergency space suit (just in case)",
        ],
        "climate_collapse": [
            "Water filtration system (for extreme weather events)",
            "Solar-powered generator",
            "Drought-resistant seeds",
            "Flood insurance (if still available)",
            "Extreme weather survival guide",
            "Portable air purifier (for dust storms/smog)",
        ],
    }
    return scenario_items.get(scenario.lower(), [])

def get_location_specific_items(location):
    """Returns items specific to a given location type."""
    location_items = {
        "urban": [
            "Bolt cutters (for navigating locked areas)",
            "Grappling hook (for vertical traversal)",
            "Discreet backpack (to blend in)",
            "Knowledge of subway/sewer systems",
            "Barricade materials (plywood, sandbags)",
            "Rooftop access tools",
        ],
        "rural": [
            "Hunting/fishing gear",
            "Gardening tools and seeds",
            "Knowledge of local flora/fauna (edible/poisonous)",
            "Off-road vehicle maintenance kit",
            "Wood-cutting tools (axe, saw)",
            "Animal traps",
        ],
        "coastal": [
            "Life raft or inflatable boat",
            "Waterproof containers",
            "Fishing nets and tackle",
            "Flare gun",
            "Desalination kit",
            "Knowledge of tides and currents",
        ],
        "mountain": [
            "Climbing gear",
            "Warm, layered clothing",
            "Snowshoes or skis (seasonal)",
            "Avalanche beacon (if applicable)",
            "Shelter building materials (tarp, rope)",
            "High-altitude sickness medication",
        ],
    }
    return location_items.get(location.lower(), [])

def generate_checklist(scenario="default", location="default"):
    """Generates a comprehensive apocalypse preparedness checklist."""
    checklist = set(get_base_checklist())
    checklist.update(get_scenario_specific_items(scenario))
    checklist.update(get_location_specific_items(location))
    return sorted(list(checklist))

def main():
    parser = argparse.ArgumentParser(
        description="Generate a personalized apocalypse preparedness checklist.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--scenario",
        type=str,
        default="default",
        help=textwrap.dedent("""
            Specify the apocalypse scenario (e.g., zombie, nuclear, ai_uprising, alien_invasion, climate_collapse).
            Default: general preparedness.
        """)
    )
    parser.add_argument(
        "--location",
        type=str,
        default="default",
        help=textwrap.dedent("""
            Specify your location type (e.g., urban, rural, coastal, mountain).
            Default: general preparedness.
        """)
    )
    args = parser.parse_args()

    print(f"--- Apocalypse Preparedness Checklist ---")
    print(f"Scenario: {args.scenario.replace('_', ' ').title()}")
    print(f"Location: {args.location.title()}")
    print("-" * 40)

    checklist_items = generate_checklist(args.scenario, args.location)

    for i, item in enumerate(checklist_items, 1):
        print(f"{i}. {item}")
    print("-" * 40)
    print("Stay safe out there, survivor!")

if __name__ == "__main__":
    main()
