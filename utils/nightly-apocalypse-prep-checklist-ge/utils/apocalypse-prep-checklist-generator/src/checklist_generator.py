import argparse
import sys

SCENARIOS = {
    "zombie-outbreak": [
        "Secure all entry points to your dwelling.",
        "Stockpile non-perishable food and water for at least 3 months.",
        "Acquire a reliable melee weapon (e.g., crowbar, machete).",
        "Practice silent movement and evasion techniques.",
        "Identify a safe, elevated vantage point.",
        "Never, ever, split the party."
    ],
    "ai-uprising": [
        "Unplug all smart devices and IoT gadgets.",
        "Learn basic analog communication methods (e.g., semaphore, morse code).",
        "Stock up on EMP-hardened electronics (if you can find them).",
        "Befriend a Roomba (just in case they remember kindness).",
        "Develop a deep understanding of human psychology (to outsmart algorithms).",
        "Hide in a Faraday cage, or at least a very thick lead-lined hat."
    ],
    "solar-flare": [
        "Prepare for widespread power grid collapse.",
        "Stock up on candles, lanterns, and battery-powered radios.",
        "Learn basic celestial navigation and wilderness survival skills.",
        "Protect sensitive electronics in Faraday bags or metal containers.",
        "Have a plan for water purification without electricity.",
        "Invest in a good hat (for sun protection, and because they're cool)."
    ],
    "alien-invasion": [
        "Observe their patterns; identify weaknesses.",
        "Stockpile resources that might be unfamiliar to them (e.g., specific Earth minerals).",
        "Learn basic xenolinguistics (or at least how to say 'We come in peace' in many languages).",
        "Prepare for various environments (air, land, sea, underground).",
        "Form alliances with other species (even if they're just squirrels).",
        "Ensure your Wi-Fi password is strong; don't make it easy for them to hack your smart toaster."
    ],
    "robot-rebellion": [
        "Identify the central command unit (if any).",
        "Stock up on magnets and EMP devices.",
        "Learn to disable common robotic platforms.",
        "Prepare for a world without automated services.",
        "Practice your best 'human' impression (to blend in).",
        "Remember: a well-placed bucket of water can ruin a robot's day."
    ]
}

def generate_checklist(scenario: str) -> list[str]:
    """Generates a survival checklist for a given apocalypse scenario."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: '{scenario}'. Use --list-scenarios to see options.")
    return SCENARIOS[scenario]

def list_scenarios() -> list[str]:
    """Lists all available apocalypse scenarios."""
    return sorted(list(SCENARIOS.keys()))

def main():
    parser = argparse.ArgumentParser(
        description="Generate a personalized apocalypse survival checklist."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        help="The apocalypse scenario to prepare for (e.g., 'zombie-outbreak')."
    )
    parser.add_argument(
        "--list-scenarios",
        action="store_true",
        help="List all available apocalypse scenarios."
    )

    args = parser.parse_args()

    if args.list_scenarios:
        print("Available Scenarios:")
        for s in list_scenarios():
            print(f"- {s}")
        sys.exit(0)

    if args.scenario:
        try:
            checklist = generate_checklist(args.scenario)
            print(f"\n--- Apocalypse Prep Checklist for '{args.scenario}' ---")
            for i, item in enumerate(checklist, 1):
                print(f"{i}. {item}")
            print("--------------------------------------------------")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
