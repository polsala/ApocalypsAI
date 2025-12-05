import argparse
import math
import sys

# Whimsical plant data for post-apocalyptic gardening
# 'space' is in arbitrary units (e.g., square meters/feet per plant)
# 'resilience' is a subjective rating for surviving harsh conditions
PLANT_DATA = {
    "Mutant Tomato (Red Dawn)": {"space": 2.0, "light": ["sun"], "soil": ["loamy"], "yield": "high", "resilience": "Excellent"},
    "Glow-in-the-Dark Carrot": {"space": 0.5, "light": ["sun", "partial"], "soil": ["sandy", "loamy"], "yield": "medium", "resilience": "Good"},
    "Shadow Lettuce": {"space": 1.0, "light": ["partial", "shade"], "soil": ["loamy", "clay"], "yield": "medium", "resilience": "Excellent"},
    "Rad-ish (Quick Sprout)": {"space": 0.3, "light": ["sun", "partial"], "soil": ["sandy", "loamy"], "yield": "fast", "resilience": "Good"},
    "Survival Beans (Climbing)": {"space": 1.5, "light": ["sun"], "soil": ["loamy", "clay"], "yield": "high", "resilience": "Excellent"},
    "Iron-Leaf Spinach": {"space": 0.7, "light": ["partial", "shade"], "soil": ["loamy"], "yield": "medium", "resilience": "Excellent"},
    "Dusty Potato (Tuber of Hope)": {"space": 1.2, "light": ["sun", "partial"], "soil": ["loamy", "sandy"], "yield": "high", "resilience": "Excellent"},
    "Wasteland Wheat": {"space": 0.2, "light": ["sun"], "soil": ["loamy", "clay", "sandy"], "yield": "high", "resilience": "Exceptional"},
    "Scavenger Squash": {"space": 3.0, "light": ["sun"], "soil": ["loamy", "sandy"], "yield": "very high", "resilience": "Good"},
}

def plan_garden(width: float, length: float, light: str, soil: str) -> dict:
    """
    Plans a garden based on dimensions, light, and soil conditions.

    Args:
        width: The width of the garden plot.
        length: The length of the garden plot.
        light: The light condition ('sun', 'partial', 'shade').
        soil: The soil type ('sandy', 'loamy', 'clay').

    Returns:
        A dictionary where keys are plant names and values are the
        estimated number of plants that can fit, or an empty dict if no plants fit.
    """
    if not all(isinstance(arg, (int, float)) and arg > 0 for arg in [width, length]):
        raise ValueError("Width and length must be positive numbers.")
    if light not in ["sun", "partial", "shade"]:
        raise ValueError("Light must be 'sun', 'partial', or 'shade'.")
    if soil not in ["sandy", "loamy", "clay"]:
        raise ValueError("Soil must be 'sandy', 'loamy', or 'clay'.")

    total_area = width * length
    recommendations = {}

    for plant_name, data in PLANT_DATA.items():
        if light in data["light"] and soil in data["soil"]:
            space_per_plant = data["space"]
            if space_per_plant > 0:
                num_plants = math.floor(total_area / space_per_plant)
                if num_plants > 0:
                    recommendations[plant_name] = num_plants
    return recommendations

def main():
    parser = argparse.ArgumentParser(
        description="Gloom & Bloom Garden Planner: Cultivate hope in the rubble!"
    )
    parser.add_argument(
        "--width",
        type=float,
        required=True,
        help="Width of the garden plot (e.g., meters, feet). Must be positive.",
    )
    parser.add_argument(
        "--length",
        type=float,
        required=True,
        help="Length of the garden plot (e.g., meters, feet). Must be positive.",
    )
    parser.add_argument(
        "--light",
        type=str,
        choices=["sun", "partial", "shade"],
        required=True,
        help="Predominant light condition: 'sun', 'partial', or 'shade'.",
    )
    parser.add_argument(
        "--soil",
        type=str,
        choices=["sandy", "loamy", "clay"],
        required=True,
        help="Primary soil type: 'sandy', 'loamy', or 'clay'.",
    )

    args = parser.parse_args()

    try:
        recommendations = plan_garden(args.width, args.length, args.light, args.soil)

        if recommendations:
            print(f"\n--- Gloom & Bloom Garden Plan for {args.width}x{args.length} units ({args.light}, {args.soil}) ---")
            print(f"Total cultivable area: {args.width * args.length:.2f} units²\n")
            print("Recommended Resilient Plants:")
            for plant, count in recommendations.items():
                plant_info = PLANT_DATA[plant]
                print(f"  - {plant}: {count} units (Space per plant: {plant_info['space']:.1f}, Resilience: {plant_info['resilience']})")
            print("\nMay your harvest be bountiful and your spirit unyielding!")
        else:
            print(f"\nNo suitable plants found for a {args.width}x{args.length} unit garden with {args.light} light and {args.soil} soil.")
            print("Perhaps try different conditions or consult the ancient texts for forgotten flora.")
        sys.exit(0)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Catch any other unexpected errors during execution
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
