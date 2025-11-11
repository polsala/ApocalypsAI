import argparse
import sys

def _get_base_checklist_items():
    return {
        "immediate": [
            "Secure your dwelling: Barricade doors and windows with heavy furniture.",
            "Gather essential supplies: Water (3 days supply per person), non-perishable food, first-aid kit.",
            "Establish communication plan: Designate a rally point and check-in times with family/friends.",
            "Stay informed: Monitor emergency broadcasts (if available)."
        ],
        "mid_term": [
            "Scavenge for resources: Prioritize water filters, medical supplies, durable tools.",
            "Fortify your position: Reinforce entry points, create escape routes.",
            "Learn basic self-defense: Improvise weapons, practice evasion tactics.",
            "Conserve power: Limit use of electronics, rely on manual tools."
        ],
        "long_term": [
            "Seek a safer location: Consider moving to higher ground or less populated areas.",
            "Cultivate food sources: Start a small garden if feasible, learn foraging.",
            "Form alliances: Connect with other survivors for mutual protection and resource sharing.",
            "Maintain morale: Find ways to stay positive and mentally resilient."
        ]
    }

def _get_scenario_specific_items(scenario):
    items = {
        "zombie_outbreak": {
            "immediate": [
                "Ensure all entry points are sealed against the undead.",
                "Prepare blunt and bladed melee weapons; firearms if available and trained."
            ],
            "mid_term": [
                "Practice silent movement and evasion techniques.",
                "Learn basic zombie anatomy (headshots are key!)."
            ],
            "long_term": [
                "Establish a secure, defensible perimeter.",
                "Develop a system for waste disposal to avoid attracting attention."
            ]
        },
        "meteor_strike": {
            "immediate": [
                "Seek immediate shelter underground or in structurally sound buildings.",
                "Protect against fallout: seal windows, cover vents, prepare for dust."
            ],
            "mid_term": [
                "Assess structural damage and potential hazards.",
                "Prioritize air filtration and radiation protection if applicable."
            ],
            "long_term": [
                "Prepare for a 'nuclear winter' scenario: focus on warmth, light, and stored food.",
                "Begin long-term debris clearing and rebuilding efforts."
            ]
        },
        "ai_uprising": {
            "immediate": [
                "Disconnect from all networked devices; disable smart home tech.",
                "Destroy any AI-controlled drones or robots in your vicinity."
            ],
            "mid_term": [
                "Avoid digital communication; rely on analog methods (radio, messengers).",
                "Seek out EMP-proof shelters or Faraday cages."
            ],
            "long_term": [
                "Learn to live off-grid and without advanced technology.",
                "Form resistance cells focused on disrupting AI infrastructure."
            ]
        },
        "solar_flare": {
            "immediate": [
                "Unplug all sensitive electronics immediately to prevent EMP damage.",
                "Prepare for widespread power outages and communication blackouts."
            ],
            "mid_term": [
                "Rely on analog tools: compass, paper maps, hand-crank radios.",
                "Protect critical electronics in Faraday bags/cages if not already done."
            ],
            "long_term": [
                "Rebuild infrastructure with EMP-resistant components.",
                "Develop sustainable, off-grid power solutions."
            ]
        }
    }
    return items.get(scenario, {})

def _get_location_specific_notes(location):
    notes = {
        "urban": [
            "High population density means more immediate threats but also more potential resources.",
            "Focus on stealth and avoiding main thoroughfares.",
            "Utilize rooftops and elevated structures for observation and movement."
        ],
        "rural": [
            "Lower population density means fewer immediate threats but also fewer readily available resources.",
            "Focus on self-sufficiency: farming, hunting, water purification.",
            "Be aware of wildlife and natural hazards."
        ],
        "suburban": [
            "A mix of urban and rural challenges. Balance resource gathering with maintaining a low profile.",
            "Secure your neighborhood perimeter if possible, or identify safe zones.",
            "Leverage existing infrastructure (e.g., community gardens, local stores) carefully."
        ]
    }
    return notes.get(location, [])

def _get_resource_level_notes(resources):
    notes = {
        "minimal": [
            "You are starting with very little; scavenging and resourcefulness are paramount.",
            "Prioritize water, basic food, and a multi-tool above all else.",
            "Consider immediate relocation to a more resource-rich or defensible area."
        ],
        "moderate": [
            "You have some existing supplies; focus on replenishing and diversifying.",
            "Consider investing in a solar charger for small electronics.",
            "Prioritize durable goods over consumables during scavenging."
        ],
        "abundant": [
            "You are well-stocked; focus on security, long-term sustainability, and helping others (cautiously).",
            "Consider setting up a robust defense system and a sustainable food/water supply.",
            "Your biggest challenge might be protecting your resources from others."
        ]
    }
    return notes.get(resources, [])

def generate_apocalypse_checklist(scenario, location, resources):
    if scenario not in _get_scenario_specific_items('zombie_outbreak'): # Check against a known scenario's keys for validation
        raise ValueError(f"Invalid scenario: {scenario}")
    if location not in _get_location_specific_notes():
        raise ValueError(f"Invalid location: {location}")
    if resources not in _get_resource_level_notes():
        raise ValueError(f"Invalid resources: {resources}")

    base_items = _get_base_checklist_items()
    scenario_items = _get_scenario_specific_items(scenario)

    checklist_output = []
    checklist_output.append(f"# Apocalypse Survival Checklist: {scenario.replace('_', ' ').title()} ({location.title()}, {resources.title()} Resources)\n")

    for category in ["immediate", "mid_term", "long_term"]:
        checklist_output.append(f"## {category.replace('_', ' ').title()} Actions:\n")
        items = base_items.get(category, []) + scenario_items.get(category, [])
        for item in items:
            checklist_output.append(f"*   {item}")
        checklist_output.append("") # Newline for spacing

    resource_notes = _get_resource_level_notes(resources)
    if resource_notes:
        checklist_output.append("## Resource Adjustments ({}):\n".format(resources.title()))
        for note in resource_notes:
            checklist_output.append(f"*   {note}")
        checklist_output.append("")

    location_notes = _get_location_specific_notes(location)
    if location_notes:
        checklist_output.append("## Location Specifics ({}):\n".format(location.title()))
        for note in location_notes:
            checklist_output.append(f"*   {note}")
        checklist_output.append("")

    checklist_output.append("---\n")
    checklist_output.append("*Stay vigilant, stay safe, and may your aim be true!*\n")

    return "\n".join(checklist_output)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a personalized apocalypse survival checklist."
    )
    parser.add_argument(
        "--scenario",
        choices=["zombie_outbreak", "meteor_strike", "ai_uprising", "solar_flare"],
        required=True,
        help="The type of apocalypse."
    )
    parser.add_argument(
        "--location",
        choices=["urban", "rural", "suburban"],
        required=True,
        help="Your current environment."
    )
    parser.add_argument(
        "--resources",
        choices=["minimal", "moderate", "abundant"],
        required=True,
        help="Your current resource level."
    )

    args = parser.parse_args()

    try:
        checklist = generate_apocalypse_checklist(
            args.scenario,
            args.location,
            args.resources
        )
        print(checklist)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
