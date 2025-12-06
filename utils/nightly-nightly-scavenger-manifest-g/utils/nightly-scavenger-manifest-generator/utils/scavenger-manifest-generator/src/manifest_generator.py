import argparse
import datetime

class ManifestGenerator:
    ITEM_DATA = {
        "food_ration": {"category": "food", "scarcity": 2, "risk": "low", "time_cost": 0.5},
        "purification_tablet": {"category": "water", "scarcity": 3, "risk": "low", "time_cost": 0.2},
        "scrap_metal": {"category": "parts", "scarcity": 1, "risk": "low", "time_cost": 0.3},
        "medical_kit": {"category": "medical", "scarcity": 4, "risk": "medium", "time_cost": 1.0},
        "circuit_board": {"category": "parts", "scarcity": 5, "risk": "high", "time_cost": 1.5},
        "fresh_water_source": {"category": "water", "scarcity": 1, "risk": "medium", "time_cost": 0.8},
        "canned_goods": {"category": "food", "scarcity": 2, "risk": "low", "time_cost": 0.6},
        "tool_kit": {"category": "tools", "scarcity": 3, "risk": "medium", "time_cost": 1.2},
        "rare_herb": {"category": "medical", "scarcity": 5, "risk": "high", "time_cost": 0.7},
        "morale_booster_toy": {"category": "morale", "scarcity": 3, "risk": "low", "time_cost": 0.4},
        "survival_guide": {"category": "tools", "scarcity": 4, "risk": "low", "time_cost": 0.9},
        "empty_fuel_can": {"category": "parts", "scarcity": 2, "risk": "medium", "time_cost": 0.5},
    }

    RISK_LEVELS = {"low": 1, "medium": 2, "high": 3}

    def __init__(self):
        pass

    def generate_manifest(
        self,
        daily_needs: dict[str, int],
        risk_tolerance: str,
        scavenge_hours: float,
    ) -> list[dict]:
        manifest = []
        current_time_spent = 0.0
        fulfilled_needs = {category: 0 for category in daily_needs}

        # Sort items by scarcity (lower scarcity first, easier to find)
        # and then by time_cost (lower time_cost first, more efficient)
        sorted_items = sorted(
            self.ITEM_DATA.items(), 
            key=lambda item: (item[1]['scarcity'], item[1]['time_cost'])
        )

        # Convert risk tolerance to a comparable level
        max_risk_level = self.RISK_LEVELS.get(risk_tolerance.lower(), 1) # Default to low

        # Prioritize items based on needs and then other factors
        for item_name, item_info in sorted_items:
            category = item_info['category']
            item_risk_level = self.RISK_LEVELS.get(item_info['risk'].lower(), 1)

            # Check if this item fulfills a current need and we haven't met the need yet
            if category in daily_needs and fulfilled_needs[category] < daily_needs[category]:
                # Check risk tolerance
                if item_risk_level <= max_risk_level:
                    # Check if we have enough time
                    if current_time_spent + item_info['time_cost'] <= scavenge_hours:
                        manifest.append({
                            "name": item_name.replace('_', ' ').title(),
                            "category": category.title(),
                            "priority": "High", # Items directly fulfilling needs are high priority
                            "risk": item_info['risk'].title(),
                            "time_cost": item_info['time_cost']
                        })
                        current_time_spent += item_info['time_cost']
                        fulfilled_needs[category] += 1

        return manifest

def main():
    parser = argparse.ArgumentParser(
        description="Generate a daily scavenging manifest."
    )
    parser.add_argument("--food", type=int, default=0, help="Desired units of food.")
    parser.add_argument("--water", type=int, default=0, help="Desired units of water.")
    parser.add_argument("--parts", type=int, default=0, help="Desired units of repair/crafting parts.")
    parser.add_argument("--medical", type=int, default=0, help="Desired units of medical supplies.")
    parser.add_argument("--tools", type=int, default=0, help="Desired units of tools.")
    parser.add_argument("--morale", type=int, default=0, help="Desired units of morale boosters.")
    parser.add_argument(
        "--risk",
        type=str,
        choices=ManifestGenerator.RISK_LEVELS.keys(),
        default="low",
        help="Your tolerance for danger (low, medium, high).",
    )
    parser.add_argument(
        "--hours", type=float, default=8.0, help="Maximum hours for scavenging."
    )

    args = parser.parse_args()

    # Filter out non-need arguments and zero needs
    actual_needs = {}
    for category in ['food', 'water', 'parts', 'medical', 'tools', 'morale']:
        if getattr(args, category) > 0:
            actual_needs[category] = getattr(args, category)

    generator = ManifestGenerator()
    manifest = generator.generate_manifest(actual_needs, args.risk, args.hours)

    print(f"--- Scavenging Manifest for {datetime.date.today()} ---")
    print("\nPrioritized Needs:")
    if not actual_needs:
        print("- No specific needs defined.")
    else:
        for need, quantity in actual_needs.items():
            print(f"- {need.title()}: {quantity} units")
    print(f"\nRisk Tolerance: {args.risk.title()}")
    print(f"Time Available: {args.hours} hours")

    print("\n--- Your Mission Checklist ---")
    if not manifest:
        print("No items found matching your criteria. Perhaps adjust needs, risk, or time?")
    else:
        total_time = 0.0
        for i, item in enumerate(manifest):
            print(
                f"{i+1}. {item['name']} ({item['category']}) - Priority: {item['priority']}, "
                f"Risk: {item['risk']}, Time: {item['time_cost']}h"
            )
            total_time += item['time_cost']
        print(f"\nTotal Estimated Time: {total_time:.1f} hours")

    print("\nGood luck, survivor! May your hauls be plentiful and your encounters minimal.")

if __name__ == "__main__":
    main()
