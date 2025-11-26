import argparse
import json
import sys
from typing import List, Dict, Any

class Plant:
    """Represents a single plant type with its properties."""
    def __init__(self, name: str, space_sqm: float, yield_units: int, climate_zones: List[str]):
        self.name = name
        self.space_sqm = space_sqm
        self.yield_units = yield_units
        self.climate_zones = [c.lower() for c in climate_zones]

    def __repr__(self):
        return f"Plant(name='{self.name}', space_sqm={self.space_sqm}, yield_units={self.yield_units})"

    def get_value_per_sqm(self) -> float:
        """Calculates the yield value per square meter for the plant."""
        return self.yield_units / self.space_sqm if self.space_sqm > 0 else 0

def load_seed_data(filepath: str) -> List[Plant]:
    """Loads seed data from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        plants = []
        for item in raw_data:
            plants.append(Plant(
                name=item['name'],
                space_sqm=float(item['space_sqm']),
                yield_units=int(item['yield_units']),
                climate_zones=item['climate_zones']
            ))
        return plants
    except FileNotFoundError:
        print(f"Error: Seed data file not found at {filepath}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in seed data file {filepath}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing key in seed data: {e}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, TypeError) as e:
        print(f"Error: Invalid data type in seed data: {e}", file=sys.stderr)
        sys.exit(1)

def plan_garden(available_area_sqm: float, climate_zone: str, seed_inventory: List[Plant]) -> List[Dict[str, Any]]:
    """
    Plans a garden layout based on available area, climate, and seed inventory.
    Prioritizes plants with higher yield per square meter.
    """
    climate_zone = climate_zone.lower()
    suitable_plants = [
        plant for plant in seed_inventory
        if climate_zone in plant.climate_zones
    ]

    # Sort plants by value (yield per square meter) in descending order
    suitable_plants.sort(key=lambda p: p.get_value_per_sqm(), reverse=True)

    planting_plan = []
    remaining_area = available_area_sqm

    for plant in suitable_plants:
        if remaining_area <= 0:
            break

        # Calculate how many of this plant can fit
        num_plants = int(remaining_area // plant.space_sqm)

        if num_plants > 0:
            planting_plan.append({
                'plant': plant.name,
                'count': num_plants,
                'total_space_used_sqm': num_plants * plant.space_sqm,
                'estimated_total_yield': num_plants * plant.yield_units
            })
            remaining_area -= num_plants * plant.space_sqm

    return planting_plan

def main():
    parser = argparse.ArgumentParser(
        description="Gloom-to-Bloom Garden Planner: Optimize your survival garden layout."
    )
    parser.add_argument(
        "--area",
        type=float,
        required=True,
        help="Total available garden area in square meters."
    )
    parser.add_argument(
        "--climate",
        type=str,
        required=True,
        help="Dominant climate zone (e.g., 'temperate', 'arid', 'cold')."
    )
    parser.add_argument(
        "--seeds",
        type=str,
        required=True,
        help="Path to a JSON file containing your seed inventory."
    )

    args = parser.parse_args()

    seed_inventory = load_seed_data(args.seeds)
    if not seed_inventory:
        print("No seeds loaded or available. Cannot plan a garden.", file=sys.stderr)
        sys.exit(2) # No-op, nothing to change

    plan = plan_garden(args.area, args.climate, seed_inventory)

    if not plan:
        print(f"Could not create a viable garden plan for {args.area} sqm in {args.climate} climate with available seeds.", file=sys.stderr)
        sys.exit(2) # No-op, nothing to change

    print("--- Gloom-to-Bloom Garden Plan ---")
    print(f"Available Area: {args.area:.2f} sqm")
    print(f"Climate Zone: {args.climate.capitalize()}")
    print("\nPlanting Details:")
    total_yield = 0
    total_space_used = 0
    for item in plan:
        print(f"  - {item['count']}x {item['plant']} (uses {item['total_space_used_sqm']:.2f} sqm, est. yield: {item['estimated_total_yield']} units)")
        total_yield += item['estimated_total_yield']
        total_space_used += item['total_space_used_sqm']

    print(f"\nSummary:")
    print(f"  Total estimated yield: {total_yield} units")
    print(f"  Total space utilized: {total_space_used:.2f} sqm")
    print(f"  Remaining unused space: {args.area - total_space_used:.2f} sqm")

if __name__ == "__main__":
    main()
