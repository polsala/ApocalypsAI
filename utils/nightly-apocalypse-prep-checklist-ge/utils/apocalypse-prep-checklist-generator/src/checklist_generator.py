import sys
from typing import List, Dict

def get_base_checklist() -> List[str]:
    """Returns a universal set of apocalypse preparedness items."""
    return [
        "Stockpile non-perishable food (3-month supply)",
        "Ensure access to clean water (or purification tablets)",
        "First-aid kit (fully stocked)",
        "Emergency communication device (hand-crank radio, satellite phone)",
        "Backup power source (solar charger, generator)",
        "Important documents (physical and digital backups)",
        "Cash in small denominations",
        "Multi-tool or utility knife",
        "Warm clothing and blankets",
        "Self-defense training (or at least a sturdy stick)",
        "Develop a family emergency plan and meeting points",
        "Learn basic survival skills (fire starting, shelter building)",
    ]

def get_scenario_specific_items() -> Dict[str, List[str]]:
    """Returns a dictionary of items specific to different apocalypse scenarios."""
    return {
        "zombie_outbreak": [
            "Sharpen all bladed weapons (machetes, katanas)",
            "Reinforce all entry points (barricades, traps)",
            "Practice headshots (on targets, please!)",
            "Identify safe zones and escape routes",
            "Stock up on brain-repellent spray (just in case)",
        ],
        "ai_uprising": [
            "Unplug all smart devices (especially toasters)",
            "Learn to communicate without electronics (smoke signals, semaphore)",
            "Develop a disguise that fools facial recognition (hats, sunglasses, glitter)",
            "Practice disabling drones with a well-aimed rock",
            "Hide from surveillance cameras (and sentient vacuum cleaners)",
        ],
        "solar_flare": [
            "EMP-proof essential electronics (Faraday cage for your Walkman)",
            "Stock up on candles, oil lamps, and matches",
            "Learn celestial navigation (stars are your new GPS)",
            "Prepare for grid-down living (no internet, no Netflix)",
            "Invest in a good pair of sunglasses (for the extra-bright sun)",
        ],
        # 'general_catastrophe' will just use the base items
    }

def generate_checklist(scenario: str = "general_catastrophe") -> List[str]:
    """
    Generates a comprehensive apocalypse preparedness checklist for a given scenario.

    Args:
        scenario (str): The specific apocalypse scenario (e.g., "zombie_outbreak", "ai_uprising").

    Returns:
        List[str]: A list of preparedness items.
    """
    base_items = get_base_checklist()
    scenario_items = get_scenario_specific_items().get(scenario.lower(), [])
    
    # Combine and remove duplicates (though unlikely for these lists)
    full_checklist = list(dict.fromkeys(base_items + scenario_items))
    return full_checklist

if __name__ == "__main__":
    chosen_scenario = sys.argv[1] if len(sys.argv) > 1 else "general_catastrophe"
    
    print(f"--- Apocalypse Preparedness Checklist for: {chosen_scenario.replace('_', ' ').title()} ---")
    checklist = generate_checklist(chosen_scenario)
    for i, item in enumerate(checklist, 1):
        print(f"{i}. {item}")
    print("\nStay safe out there, survivor!")
