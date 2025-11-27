import argparse
import json
from typing import List, Dict, Any

# Mock rationale: In a real-world scenario, this catalog might be loaded from a database or a configuration file.
# For a self-contained utility, hardcoding it makes tests deterministic and avoids external dependencies.
PLANT_CATALOG: List[Dict[str, Any]] = [
    {
        "name": "Radish",
        "type": "vegetable",
        "growth_time_days": 30,
        "preferred_climate": ["temperate", "cool"],
        "preferred_soil": ["loamy", "sandy"],
        "space_required_sqft": 0.2,
        "yield_per_sqft": 0.5, # kg
        "notes": "Fast-growing, good for quick harvests."
    },
    {
        "name": "Tomato",
        "type": "vegetable",
        "growth_time_days": 90,
        "preferred_climate": ["warm", "temperate"],
        "preferred_soil": ["loamy", "clay"],
        "space_required_sqft": 2.0,
        "yield_per_sqft": 3.0,
        "notes": "Needs support, sun-loving."
    },
    {
        "name": "Potato",
        "type": "vegetable",
        "growth_time_days": 120,
        "preferred_climate": ["temperate", "cool"],
        "preferred_soil": ["sandy", "loamy"],
        "space_required_sqft": 1.5,
        "yield_per_sqft": 2.5,
        "notes": "High calorie, needs hilling."
    },
    {
        "name": "Basil",
        "type": "herb",
        "growth_time_days": 60,
        "preferred_climate": ["warm", "temperate"],
        "preferred_soil": ["loamy"],
        "space_required_sqft": 0.5,
        "yield_per_sqft": 0.1,
        "notes": "Aromatic, repels some pests."
    },
    {
        "name": "Sunflower",
        "type": "flower",
        "growth_time_days": 90,
        "preferred_climate": ["warm", "temperate"],
        "preferred_soil": ["any"],
        "space_required_sqft": 3.0,
        "yield_per_sqft": 0.2, # kg of seeds
        "notes": "Provides seeds and visual morale boost."
    }
]

def plan_garden(
    plant_catalog: List[Dict[str, Any]],
    climate_zone: str,
    soil_type: str,
    available_space_sqft: float
) -> Dict[str, Any]:
    """
    Generates a garden planting plan based on environmental conditions and available space.

    Args:
        plant_catalog: A list of dictionaries, each describing a plant.
        climate_zone: The current climate zone (e.g., "warm", "temperate", "cool").
        soil_type: The type of soil available (e.g., "loamy", "sandy", "clay").
        available_space_sqft: The total square footage available for planting.

    Returns:
        A dictionary containing the planting plan and summary statistics.
    """
    suitable_plants = []
    for plant in plant_catalog:
        climate_match = climate_zone.lower() in [c.lower() for c in plant["preferred_climate"]]
        soil_match = soil_type.lower() in [s.lower() for s in plant["preferred_soil"]] or "any" in [s.lower() for s in plant["preferred_soil"]]

        if climate_match and soil_match:
            suitable_plants.append(plant)

    # Prioritize faster-growing plants for quicker yield in an apocalyptic scenario
    suitable_plants.sort(key=lambda p: p["growth_time_days"])

    planting_plan = []
    current_space_used = 0.0
    total_estimated_yield = 0.0

    for plant in suitable_plants:
        if plant["space_required_sqft"] <= 0: # Avoid division by zero or infinite loops
            continue

        remaining_space = available_space_sqft - current_space_used
        if remaining_space <= 0:
            break

        # Calculate how many of this plant can fit
        quantity = int(remaining_space / plant["space_required_sqft"])
        if quantity == 0:
            continue

        space_for_this_plant = quantity * plant["space_required_sqft"]
        estimated_yield_for_this_plant = quantity * plant["yield_per_sqft"]

        planting_plan.append({
            "name": plant["name"],
            "quantity": quantity,
            "space_used_sqft": round(space_for_this_plant, 2),
            "estimated_yield_kg": round(estimated_yield_for_this_plant, 2),
            "notes": plant["notes"]
        })
        current_space_used += space_for_this_plant
        total_estimated_yield += estimated_yield_for_this_plant

    return {
        "climate_zone": climate_zone,
        "soil_type": soil_type,
        "available_space_sqft": round(available_space_sqft, 2),
        "planting_plan": planting_plan,
        "total_space_used_sqft": round(current_space_used, 2),
        "total_estimated_yield_kg": round(total_estimated_yield, 2),
        "remaining_space_sqft": round(available_space_sqft - current_space_used, 2),
        "notes": "Plan prioritizes faster-growing plants suitable for specified conditions. Yields are estimates."
    }

def main():
    parser = argparse.ArgumentParser(
        description="Gloom & Bloom Garden Planner: Suggests a planting plan for post-apocalyptic survival."
    )
    parser.add_argument(
        "--climate",
        type=str,
        required=True,
        help="Current climate zone (e.g., 'warm', 'temperate', 'cool')."
    )
    parser.add_argument(
        "--soil",
        type=str,
        required=True,
        help="Type of soil available (e.g., 'loamy', 'sandy', 'clay')."
    )
    parser.add_argument(
        "--space",
        type=float,
        required=True,
        help="Total square footage available for planting."
    )

    args = parser.parse_args()

    plan = plan_garden(PLANT_CATALOG, args.climate, args.soil, args.space)
    print(json.dumps(plan, indent=2))

if __name__ == "__main__":
    main()
