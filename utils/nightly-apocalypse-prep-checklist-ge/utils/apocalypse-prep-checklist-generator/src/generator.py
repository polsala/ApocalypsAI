import argparse
import sys

SCENARIOS = {
    "zombie": [
        "Secure all entry points (doors, windows, vents). Seriously.",
        "Stockpile non-perishable food and water (at least 3-day supply per person).",
        "Learn basic first aid and wound care (zombie bites are messy).",
        "Identify a safe, defensible location (high ground, limited access).",
        "Acquire blunt force trauma weapons (crowbar, baseball bat) and practice headshots (on targets, please!).",
        "Have a bug-out bag ready with essentials for quick evacuation.",
        "Establish a communication plan with your survival group (no cell service).",
        "Practice stealth and evasion techniques.",
        "Remember: Cardio is key."
    ],
    "meteor": [
        "Locate the nearest sturdy underground shelter or reinforced structure.",
        "Stockpile water purification tablets and a large supply of bottled water.",
        "Prepare for prolonged darkness and dust; gather flashlights, headlamps, and extra batteries.",
        "Have a supply of N95 masks or similar for airborne debris.",
        "Secure important documents in waterproof containers.",
        "Learn basic astronomy (to spot the next one coming, or just for fun).".
        "Develop a plan for communication after potential infrastructure collapse.",
        "Stock up on comfort items: books, games, a good sense of humor."
    ],
    "ai-uprising": [
        "Unplug all non-essential smart devices and disconnect from the internet.",
        "Learn to communicate without digital means (flags, smoke signals, carrier pigeons).",
        "Stockpile EMP-hardened electronics (if you can find them) or go fully analog.",
        "Practice your best human impression; avoid looking suspicious around automated systems.",
        "Develop skills that AIs can't easily replicate (e.g., empathy, abstract art, sarcasm).",
        "Have a 'dumb' phone or satellite phone for emergencies (if it still works).".
        "Prepare for a world where your toaster might judge you.",
        "Learn to code in assembly, just in case you need to talk to a very old machine."
    ],
    "solar-flare": [
        "Charge all portable electronic devices to 100% immediately.",
        "Have a Faraday cage ready for sensitive electronics (phones, radios, medical devices).",
        "Stock up on analog communication tools: walkie-talkies, shortwave radio, signal mirrors.",
        "Prepare for widespread power grid collapse and long-term outages.",
        "Gather non-electric cooking methods (camping stove, grill) and fuel.",
        "Ensure you have a good supply of cash in small denominations.",
        "Learn basic navigation without GPS (map and compass).".
        "Prepare for a return to simpler times, perhaps with more stargazing."
    ],
    "default": [
        "Emergency food & water (at least 3-day supply per person).",
        "First aid kit with essential medications.",
        "Flashlight, headlamp, and extra batteries.",
        "Multi-tool or utility knife.",
        "Copies of important documents (ID, insurance, deeds) in a waterproof bag.",
        "Cash in small denominations.",
        "Whistle for signaling help.",
        "Dust mask or bandana for air filtration.",
        "Manual can opener.",
        "Local maps (paper, not digital).".
        "A positive attitude (it helps, really!)."
    ]
}

def generate_checklist(scenario_key: str) -> list[str]:
    """
    Generates a preparedness checklist for a given scenario.
    If the scenario is unknown, returns the 'default' checklist.
    """
    return SCENARIOS.get(scenario_key.lower(), SCENARIOS["default"])

def main():
    parser = argparse.ArgumentParser(
        description="Generate an apocalypse preparedness checklist."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        default="default",
        help="The apocalypse scenario (e.g., zombie, meteor, ai-uprising, solar-flare, default)."
    )

    args = parser.parse_args()
    scenario = args.scenario.lower()

    checklist = generate_checklist(scenario)

    print(f"---\n--- Apocalypse Prep Checklist: {scenario.replace('-', ' ').title()} ---
")
    for i, item in enumerate(checklist):
        print(f"{i+1}. {item}")
    print("\nStay vigilant, survivor!")

if __name__ == "__main__":
    main()
