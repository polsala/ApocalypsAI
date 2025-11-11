import argparse
import sys

SCENARIOS = {
    "zombie": [
        "Secure a safe house with multiple exits.",
        "Stockpile non-perishable food and water (3-month supply).",
        "Gather first-aid supplies and learn basic wound care.",
        "Acquire sturdy blunt weapons (crowbar, baseball bat).",
        "Practice silent movement and evasion tactics.",
        "Identify reliable communication methods (walkie-talkies, ham radio).",
        "Establish a rendezvous point with trusted allies."
    ],
    "meteor": [
        "Prepare an underground shelter or reinforced basement.",
        "Stockpile long-term food and water purification tablets.",
        "Gather dust masks, goggles, and protective clothing.",
        "Ensure backup power sources (solar, hand-crank generator).",
        "Learn basic astronomy to track potential impacts (just kidding, mostly).",
        "Have a plan for dealing with widespread infrastructure collapse.",
        "Collect seeds for post-impact agriculture."
    ],
    "ai-uprising": [
        "Unplug all non-essential smart devices.",
        "Learn to communicate without digital means (smoke signals, carrier pigeons).",
        "Develop skills in EMP-proof technology (analog radios, mechanical tools).",
        "Stockpile Faraday cages for sensitive electronics.",
        "Practice critical thinking to discern AI propaganda.",
        "Form alliances with other humans (trust no bot).",
        "Learn to code in assembly (just in case you need to hack a toaster).".strip()
    ],
    "solar-flare": [
        "Prepare for widespread power grid failure (EMP-resistant electronics).",
        "Stockpile non-electric cooking and heating methods (wood stove, camp stove).",
        "Gather cash and barter items (digital currency will be useless).",
        "Have a physical map and compass; GPS will be down.",
        "Learn basic survival skills (fire starting, shelter building).",
        "Protect sensitive electronics in Faraday cages.",
        "Prepare for potential communication blackouts."
    ],
    "general": [
        "Assemble a 72-hour emergency kit (Go-Bag).",
        "Store at least 2 weeks of food and water per person.",
        "Have a family emergency plan and practice it.",
        "Learn basic first aid and CPR.",
        "Keep important documents in a waterproof, fireproof container.",
        "Maintain a supply of essential medications.",
        "Ensure you have multiple ways to get news and weather alerts."
    ]
}

def generate_checklist(scenario_name: str) -> list[str]:
    """Generates a preparedness checklist for a given scenario."""
    return SCENARIOS.get(scenario_name.lower(), [])

def main():
    parser = argparse.ArgumentParser(
        description="Generate a preparedness checklist for various apocalyptic scenarios."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        default="general",
        help=f"Choose a scenario: {', '.join(SCENARIOS.keys())}. Default is 'general'."
    )

    args = parser.parse_args()
    scenario = args.scenario.lower()

    if scenario not in SCENARIOS:
        print(f"Error: Unknown scenario '{scenario}'. Available scenarios: {', '.join(SCENARIOS.keys())}", file=sys.stderr)
        sys.exit(1)

    checklist = generate_checklist(scenario)

    print(f"--- Apocalypse Prep Checklist: {scenario.replace('-', ' ').title()} ---")
    if not checklist:
        print("No specific checklist items for this scenario. Try 'general'.")
    else:
        for i, item in enumerate(checklist, 1):
            print(f"{i}. {item}")

if __name__ == "__main__":
    main()
