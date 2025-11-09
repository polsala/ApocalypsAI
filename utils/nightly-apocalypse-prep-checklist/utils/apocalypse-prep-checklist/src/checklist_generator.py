import argparse

class ChecklistGenerator:
    def __init__(self):
        self.base_items = [
            "Water (1 gallon per person per day for 3 days)",
            "Non-perishable food (3-day supply)",
            "First aid kit",
            "Whistle (to signal for help)",
            "Dust mask (to filter contaminated air)",
            "Plastic sheeting and duct tape (to shelter-in-place)",
            "Wrench or pliers (to turn off utilities)",
            "Manual can opener",
            "Battery-powered or hand-crank radio",
            "Flashlight",
            "Extra batteries",
            "Cell phone with chargers and a backup battery",
            "Local maps",
            "Cash",
            "Important documents (copies in waterproof container)",
            "Prescription medications",
            "Infant formula and diapers (if applicable)",
            "Pet food and extra water for your pet (if applicable)",
            "Sleeping bag or warm blanket for each person",
            "Change of clothing for each person",
            "Fire extinguisher",
            "Matches in a waterproof container",
            "Feminine hygiene items and personal sanitation items",
            "Mess kit, paper cups, plates, paper towels",
            "Books, games, puzzles, or other activities for children",
        ]

        self.scenario_specific_items = {
            "zombie": [
                "Crowbar or other blunt weapon",
                "Machete or sharp blade",
                "Heavy-duty boots",
                "Bite-proof clothing (leather jacket, thick jeans)",
                "Quiet transportation (bicycle, skateboard)",
                "Medical supplies for trauma (sutures, strong painkillers)",
                "Walkie-talkies (for silent communication)",
                "Binoculars (for scouting)",
                "Map of local defensible locations",
                "A good pair of running shoes",
            ],
            "meteor": [
                "Radiation suit (if impact is nuclear)",
                "Gas mask with filters",
                "Underground shelter plans",
                "Long-term food storage (canned goods, MREs)",
                "Water purification tablets/filter",
                "Emergency shovel/pickaxe",
                "Heavy-duty tarp for debris protection",
                "Geiger counter (for radiation detection)",
                "Star chart (for navigating by night, if GPS fails)",
            ],
            "ai-uprising": [
                "EMP-shielded Faraday cage for electronics",
                "Analog communication devices (ham radio, signal mirror)",
                "Non-digital maps and compass",
                "Manual tools (no smart features)",
                "Physical books on survival and engineering",
                "EMP-resistant vehicle (older models)",
                "Knowledge of basic hacking/disabling AI systems (just kidding... mostly)",
                "A very convincing disguise (for blending in with robots)",
            ],
            "general": [] # Default for when no specific scenario is given
        }

    def generate_checklist(self, scenario: str) -> list[str]:
        scenario_key = scenario.lower().replace(" ", "-")
        specific_items = self.scenario_specific_items.get(scenario_key, [])
        
        # If a specific scenario is not found, we still provide the base items.
        # For "general", it will just be base_items.
        combined_list = sorted(list(set(self.base_items + specific_items)))
        return combined_list

def main():
    parser = argparse.ArgumentParser(
        description="Generate a customizable apocalypse survival checklist."
    )
    parser.add_argument(
        "scenario",
        nargs="?", # Makes it optional
        default="general",
        help="The type of apocalypse (e.g., 'zombie', 'meteor', 'ai-uprising', 'general'). Defaults to 'general'."
    )
    args = parser.parse_args()

    generator = ChecklistGenerator()
    checklist = generator.generate_checklist(args.scenario)

    print(f"--- Apocalypse Survival Checklist for: {args.scenario.title()} ---")
    for i, item in enumerate(checklist, 1):
        print(f"{i}. {item}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
