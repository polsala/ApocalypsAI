import argparse
import sys

# Default daily consumption rates per person
DEFAULT_CONSUMPTION_RATES = {
    'food': 2.0,
    'water': 3.0,
    'ammo': 0.1, # Represents occasional use/maintenance
    'meds': 0.05 # Represents minor injuries/preventative care
}

def calculate_needs(
    population: int,
    duration_days: int,
    current_resources: dict[str, float],
    consumption_rates: dict[str, float]
) -> dict:
    """
    Calculates resource needs and assesses survival prospects.

    Args:
        population: Number of survivors.
        duration_days: Number of days to survive.
        current_resources: Dictionary of available resources (e.g., {'food': 500}).
        consumption_rates: Dictionary of daily consumption per person (e.g., {'food': 2.0}).

    Returns:
        A dictionary containing required resources, remaining resources, and a survival verdict.
    """
    if population <= 0 or duration_days <= 0:
        return {
            'verdict': 'Cannot calculate for zero or negative population/duration.',
            'possible': False,
            'details': {}
        }

    required_resources = {}
    remaining_resources = {}
    shortfalls = {}
    surpluses = {}
    possible = True

    for resource, rate in consumption_rates.items():
        total_required = population * duration_days * rate
        required_resources[resource] = total_required

        current_amount = current_resources.get(resource, 0.0)
        remaining = current_amount - total_required
        remaining_resources[resource] = remaining

        if remaining < 0:
            possible = False
            shortfalls[resource] = abs(remaining)
        elif remaining > 0:
            surpluses[resource] = remaining

    verdict = """Survival for {duration_days} days with {population} survivors is {status}.
""".format(
        duration_days=duration_days,
        population=population,
        status="POSSIBLE" if possible else "IMPOSSIBLE"
    )

    details = {
        'required': {k: round(v, 2) for k, v in required_resources.items()},
        'current': {k: round(current_resources.get(k, 0.0), 2) for k in consumption_rates.keys()},
        'remaining': {k: round(v, 2) for k, v in remaining_resources.items()},
        'shortfalls': {k: round(v, 2) for k, v in shortfalls.items()},
        'surpluses': {k: round(v, 2) for k, v in surpluses.items()}
    }

    return {
        'verdict': verdict,
        'possible': possible,
        'details': details
    }

def main():
    parser = argparse.ArgumentParser(
        description="Post-Apocalyptic Resource Allocator: Calculate resource needs for survival."
    )
    parser.add_argument('--population', type=int, required=True, help='Number of survivors.')
    parser.add_argument('--duration-days', type=int, required=True, help='Number of days to survive.')
    parser.add_argument('--food', type=float, default=0.0, help='Current amount of food units available.')
    parser.add_argument('--water', type=float, default=0.0, help='Current amount of water units available.')
    parser.add_argument('--ammo', type=float, default=0.0, help='Current amount of ammunition units available.')
    parser.add_argument('--meds', type=float, default=0.0, help='Current amount of medical supply units available.')

    args = parser.parse_args()

    current_resources = {
        'food': args.food,
        'water': args.water,
        'ammo': args.ammo,
        'meds': args.meds
    }

    result = calculate_needs(
        args.population,
        args.duration_days,
        current_resources,
        DEFAULT_CONSUMPTION_RATES
    )

    print("\n--- Survival Report ---")
    print(result['verdict'])

    if result['possible']:
        print("\nGood news, commander! Your current scavenged supplies are sufficient.")
        if result['details']['surpluses']:
            print("You have the following surpluses:")
            for res, amount in result['details']['surpluses'].items():
                print(f"  - {res.capitalize()}: {amount:.2f} units")
    else:
        print("\nWarning, commander! Resource shortfalls detected.")
        if result['details']['shortfalls']:
            print("You are critically low on:")
            for res, amount in result['details']['shortfalls'].items():
                print(f"  - {res.capitalize()}: Need {amount:.2f} more units")

    print("\n--- Resource Breakdown ---")
    print("Required for survival:")
    for res, amount in result['details']['required'].items():
        print(f"  - {res.capitalize()}: {amount:.2f} units")

    print("Current inventory:")
    for res, amount in result['details']['current'].items():
        print(f"  - {res.capitalize()}: {amount:.2f} units")

    print("Remaining after allocation:")
    for res, amount in result['details']['remaining'].items():
        print(f"  - {res.capitalize()}: {amount:.2f} units")

    print("\n--- End Report ---")


if __name__ == '__main__':
    main()
