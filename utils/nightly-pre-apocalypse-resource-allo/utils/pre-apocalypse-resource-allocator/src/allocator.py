import math

def allocate_resources(resources: dict, survivors: list) -> tuple[dict, dict, list]:
    """
    Allocates resources among survivors based on needs and skills.

    Args:
        resources (dict): A dictionary of available resources, e.g.,
                          {"food_rations": 100, "water_bottles": 50, "medkits": 10, "tools": 5}.
        survivors (list): A list of survivor dictionaries, each with:
                          - "name" (str)
                          - "needs" (dict): e.g., {"food_rations": 2, "water_bottles": 1} per unit of time.
                          - "skills" (list): e.g., ["medic", "engineer"].

    Returns:
        tuple[dict, dict, list]:
            - allocation_plan (dict): Who gets what, e.g., {"Alice": {"food_rations": 10, ...}}.
            - remaining_resources (dict): Resources left after allocation.
            - unmet_needs (list): List of (survivor_name, resource_type, amount_needed) tuples.
    """
    allocation_plan = {s['name']: {} for s in survivors}
    remaining_resources = resources.copy()
    unmet_needs_raw = [] # To collect all unmet needs before consolidation

    # Define resource priorities (lower number = higher priority)
    resource_priority = {
        "water_bottles": 1,
        "food_rations": 2,
        "medkits": 3,
        "tools": 4,
    }

    # Define skill-based specific item assignments (not daily needs, but one-off items)
    skill_item_assignments = {
        "medic": "medkits",
        "engineer": "tools",
    }

    # 1. Fulfill essential daily needs based on priority
    # Iterate through resources by priority
    for resource_type in sorted(resource_priority, key=resource_priority.get):
        if resource_type not in remaining_resources or remaining_resources[resource_type] <= 0:
            continue

        # Iterate through survivors to fulfill their need for this resource
        for survivor in survivors:
            needed = survivor['needs'].get(resource_type, 0)
            if needed > 0:
                amount_to_allocate = min(needed, remaining_resources.get(resource_type, 0))
                if amount_to_allocate > 0:
                    allocation_plan[survivor['name']][resource_type] = \
                        allocation_plan[survivor['name']].get(resource_type, 0) + amount_to_allocate
                    remaining_resources[resource_type] -= amount_to_allocate
                if needed > amount_to_allocate:
                    unmet_needs_raw.append((survivor['name'], resource_type, needed - amount_to_allocate))

    # 2. Assign skill-specific items (one-off, if available)
    for skill, item_type in skill_item_assignments.items():
        if item_type not in remaining_resources or remaining_resources[item_type] <= 0:
            continue
        for survivor in survivors:
            if skill in survivor['skills']:
                # Assign one item if they don't already have it and it's available
                if allocation_plan[survivor['name']].get(item_type, 0) == 0 and remaining_resources[item_type] >= 1:
                    allocation_plan[survivor['name']][item_type] = 1
                    remaining_resources[item_type] -= 1

    # Consolidate unmet needs (sum amounts for same survivor/resource)
    final_unmet_needs = {}
    for name, res_type, amount in unmet_needs_raw:
        key = (name, res_type)
        final_unmet_needs[key] = final_unmet_needs.get(key, 0) + amount
    unmet_needs_list = sorted([(name, res_type, amount) for (name, res_type), amount in final_unmet_needs.items()])

    return allocation_plan, remaining_resources, unmet_needs_list

def main():
    # Example usage
    resources = {
        "food_rations": 50,
        "water_bottles": 30,
        "medkits": 5,
        "tools": 3
    }

    survivors = [
        {"name": "Alice", "needs": {"food_rations": 10, "water_bottles": 5}, "skills": ["medic"]},
        {"name": "Bob", "needs": {"food_rations": 8, "water_bottles": 4}, "skills": ["engineer"]},
        {"name": "Charlie", "needs": {"food_rations": 12, "water_bottles": 6}, "skills": ["scavenger"]},
    ]

    print("--- Initial State ---")
    print("Available Resources:", resources)
    print("Survivors:", survivors)

    allocation, remaining, unmet = allocate_resources(resources, survivors)

    print("\n--- Allocation Plan ---")
    for survivor, items in allocation.items():
        print(f"{survivor}:")
        if not items:
            print("  No resources allocated.")
        for item, amount in items.items():
            print(f"  - {item}: {amount}")

    print("\n--- Remaining Resources ---")
    for item, amount in remaining.items():
        print(f"- {item}: {amount}")

    print("\n--- Unmet Needs ---")
    if unmet:
        for name, res_type, amount in unmet:
            print(f"- {name} needs {amount} more {res_type}")
    else:
        print("All essential needs met!")

if __name__ == "__main__":
    main()
