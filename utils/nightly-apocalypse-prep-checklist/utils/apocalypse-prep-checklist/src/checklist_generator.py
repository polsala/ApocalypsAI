import argparse

BASE_ITEMS = [
    "Water (1 gallon per person per day for at least 3 days)",
    "Non-perishable food (3-day supply)",
    "First aid kit",
    "Whistle (to signal for help)",
    "Dust mask (to filter contaminated air)",
    "Plastic sheeting and duct tape (to shelter-in-place)",
    "Moist towelettes, garbage bags, and plastic ties (for personal sanitation)",
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
    "Sleeping bag or warm blanket for each person"
]

SCENARIO_SPECIFIC_ITEMS = {
    "zombie": [
        "Melee weapon (e.g., crowbar, baseball bat)",
        "Firearms and ammunition (if legally owned)",
        "Heavy-duty clothing (to prevent bites)",
        "Medical supplies for trauma (sutures, tourniquets)",
        "Bug-out bag (pre-packed escape kit)"
    ],
    "ai_uprising": [
        "EMP device (if available)",
        "Faraday cage (for electronics)",
        "Offline knowledge database (books, printed manuals)",
        "Non-digital communication methods (e.g., walkie-talkies, signal flares)",
        "Disguise/camouflage kit"
    ],
    "solar_flare": [
        "Backup power generator (non-grid dependent)",
        "Extra fuel for generator",
        "Manual tools (no reliance on electricity)",
        "Water purification tablets/filter",
        "Candles, matches, lighters"
    ],
    "economic_collapse": [
        "Physical gold, silver, or other precious metals",
        "Bartering goods (e.g., alcohol, tobacco, coffee, useful tools)",
        "Gardening seeds and tools",
        "Water purification system",
        "Self-defense training/equipment"
    ]
}

def generate_checklist(
    scenario: str,
    include_base: bool = True,
    custom_items: list[str] = None
) -> list[str]:
    """
    Generates a personalized apocalypse preparedness checklist.

    Args:
        scenario: The type of apocalypse scenario (e.g., 'zombie', 'ai_uprising').
        include_base: Whether to include general base survival items.
        custom_items: A list of additional items to include.

    Returns:
        A list of checklist items.
    """
    checklist = []

    if include_base:
        checklist.extend(BASE_ITEMS)

    scenario_items = SCENARIO_SPECIFIC_ITEMS.get(scenario.lower(), [])
    checklist.extend(scenario_items)

    if custom_items:
        checklist.extend(custom_items)

    # Remove duplicates and sort for consistency
    return sorted(list(set(checklist)))


def main():
    parser = argparse.ArgumentParser(
        description="Generate a personalized apocalypse preparedness checklist."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        required=True,
        choices=list(SCENARIO_SPECIFIC_ITEMS.keys()),
        help="Specify the apocalypse scenario (e.g., zombie, ai_uprising)."
    )
    parser.add_argument(
        "--no-base",
        action="store_true",
        help="Exclude the general base survival items from the checklist."
    )
    parser.add_argument(
        "--custom",
        nargs='*', # 0 or more arguments
        default=[],
        help="Add one or more custom items to your checklist."
    )

    args = parser.parse_args()

    checklist = generate_checklist(
        scenario=args.scenario,
        include_base=not args.no_base,
        custom_items=args.custom
    )

    print(f"\n--- Apocalypse Prep Checklist for {args.scenario.replace('_', ' ').title()} ---")
    for i, item in enumerate(checklist, 1):
        print(f"{i}. [ ] {item}")
    print("-------------------------------------------------------------------\n")


if __name__ == "__main__":
    main()
