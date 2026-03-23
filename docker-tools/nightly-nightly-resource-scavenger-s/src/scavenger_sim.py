import os
import random
from collections import defaultdict

def get_config():
    """Retrieves configuration from environment variables."""
    simulation_days = int(os.getenv('SIMULATION_DAYS', '7'))
    zones_str = os.getenv('ZONES', 'Ruined City,Abandoned Factory,Overgrown Forest')
    zones = [z.strip() for z in zones_str.split(',') if z.strip()]
    resources_per_zone = int(os.getenv('RESOURCES_PER_ZONE', '5'))
    resource_types_str = os.getenv('RESOURCE_TYPES', 'Water,Food,Scrap Metal,Medical Supplies,Fuel')
    resource_types = [r.strip() for r in resource_types_str.split(',') if r.strip()]

    if not zones:
        zones = ["Default Zone"]
    if not resource_types:
        resource_types = ["Unknown Resource"]

    return {
        'simulation_days': simulation_days,
        'zones': zones,
        'resources_per_zone': resources_per_zone,
        'resource_types': resource_types
    }

def run_simulation(config, random_choice_func=random.choice, random_randint_func=random.randint):
    """
    Runs the scavenging simulation.
    # Mock rationale: random_choice_func and random_randint_func are injected for deterministic testing.
    """
    total_resources = defaultdict(int)
    log = []

    simulation_days = config['simulation_days']
    zones = config['zones']
    resources_per_zone = config['resources_per_zone']
    resource_types = config['resource_types']

    log.append(f"--- Scavenger Bot Simulation Started ({simulation_days} days) ---")
    log.append(f"Zones: {', '.join(zones)}")
    log.append(f"Possible Resources: {', '.join(resource_types)}")
    log.append("-" * 50)

    for day in range(1, simulation_days + 1):
        log.append(f"\nDay {day}:")
        daily_finds = defaultdict(int)
        for zone in zones:
            # Simulate finding resources in a zone
            num_found = random_randint_func(0, resources_per_zone)
            if num_found > 0:
                for _ in range(num_found):
                    resource = random_choice_func(resource_types)
                    total_resources[resource] += 1
                    daily_finds[resource] += 1
        
        if daily_finds:
            for res, count in daily_finds.items():
                log.append(f"  Found {count}x {res} across zones.")
        else:
            log.append("  No resources found today. Tough luck!")

    log.append("\n" + "=" * 50)
    log.append("--- Simulation Complete ---")
    log.append("Total Resources Collected:")
    if total_resources:
        for resource, count in sorted(total_resources.items()):
            log.append(f"- {resource}: {count}")
    else:
        log.append("  No resources were found during the entire simulation.")
    log.append("=" * 50)

    return "\n".join(log)

if __name__ == "__main__":
    config = get_config()
    output = run_simulation(config)
    print(output)
