import argparse
import textwrap

class ChecklistGenerator:
    def __init__(self):
        self.scenarios = {
            "General Preparedness": [
                "5-gallon water supply per person",
                "2 weeks of non-perishable food",
                "Comprehensive first-aid kit",
                "Hand-crank radio/flashlight",
                "Emergency shelter plan (local safe zones)",
                "Multi-tool or utility knife",
                "Warm blankets/sleeping bags",
                "Cash in small denominations",
                "Important documents (copies in waterproof bag)"
            ],
            "Zombie Outbreak": [
                "Durable melee weapon (crowbar, machete)",
                "Secure perimeter plan (board up windows, reinforce doors)",
                "'Headshot Training Manual' (for target practice)",
                "Quiet footwear for stealth",
                "Emergency escape route (multiple options)",
                "Bite-resistant clothing (e.g., leather, denim)"
            ],
            "Rogue AI Uprising": [
                "EMP device (mocked, for disabling electronics)",
                "Faraday cage for sensitive electronics",
                "Offline knowledge base (books, printed maps)",
                "Analog communication devices (walkie-talkies)",
                "Disguise/camouflage for avoiding surveillance",
                "Manual override codes (if you can find them)"
            ],
            "Solar Flare Cataclysm": [
                "Backup power source (solar generator, car battery)",
                "EMP-hardened electronics (if available)",
                "Non-electric heating/cooking methods",
                "Radiation sickness medication (consult a doctor, if possible)",
                "Emergency lighting (candles, oil lamps)",
                "Protection from extreme UV (wide-brimmed hats, long sleeves)"
            ],
            "Giant Hamster Invasion": [
                "Oversized hamster wheel (for distraction/entertainment)",
                "Giant sunflower seeds (for bait/appeasement)",
                "Reinforced burrow/shelter (hamster-proof)",
                "Industrial-strength vacuum cleaner (for cleanup)",
                "Emergency giant hamster ball (for quick escape)",
                "Oversized water bottle (for hydration, or distraction)"
            ]
        }

    def get_available_scenarios(self):
        # Exclude 'General Preparedness' from the list of selectable scenarios
        return [s for s in self.scenarios.keys() if s != "General Preparedness"]

    def generate_checklist(self, scenario_name):
        if scenario_name not in self.scenarios:
            return None

        checklist_items = []

        # Add general preparedness items
        checklist_items.append("General Preparedness:")
        for item in self.scenarios["General Preparedness"]:
            checklist_items.append(f"-   ✅ {item}")

        # Add scenario-specific items
        if scenario_name != "General Preparedness": # Avoid duplicating header if scenario is general
            checklist_items.append(f"\nScenario-Specific Preparedness ({scenario_name}):")
            for item in self.scenarios[scenario_name]:
                checklist_items.append(f"-   ✅ {item}")

        return "\n".join(checklist_items)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a survival checklist for various apocalyptic scenarios."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        help="Specify the apocalypse scenario (e.g., 'Zombie Outbreak')."
    )

    args = parser.parse_args()

    generator = ChecklistGenerator()

    if args.scenario:
        if args.scenario not in generator.get_available_scenarios():
            print(f"Error: Scenario '{args.scenario}' not found.")
            print(f"Available scenarios: {', '.join(generator.get_available_scenarios())}")
            exit(1)
        
        print(f"--- Apocalypse Prep Checklist: {args.scenario} ---")
        checklist = generator.generate_checklist(args.scenario)
        print(checklist)
        print("\nStay vigilant, survivor!")
    else:
        print("Please specify a scenario using --scenario. Available scenarios:")
        for s in generator.get_available_scenarios():
            print(f"- {s}")
        exit(0)

if __name__ == "__main__":
    main()
