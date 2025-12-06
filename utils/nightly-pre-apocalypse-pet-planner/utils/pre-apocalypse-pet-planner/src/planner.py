import argparse

def generate_checklist(pet_name: str, pet_type: str, special_needs: str = None) -> str:
    """
    Generates a personalized apocalypse preparedness checklist for a pet.
    """
    pet_type_lower = pet_type.lower()
    checklist_items = []
    actions_to_take = []

    checklist_items.append(f"*   **Food**: 2 weeks supply of {pet_name}'s favorite kibble/wet food (or appropriate diet for {pet_type_lower}).")
    checklist_items.append(f"*   **Water**: 2 weeks supply of fresh water (or purification tablets/filter).")

    if special_needs:
        checklist_items.append(f"*   **Medication**: {special_needs} (2-week supply) and any necessary administration tools.")
    
    checklist_items.append(f"*   **First-Aid Kit**: Pet-specific bandages, antiseptic wipes, gauze, medical tape, paw protection, and any species-specific items.")
    checklist_items.append(f"*   **Carrier/Crate**: A secure, comfortable carrier or crate for evacuation and safe transport.")
    
    if pet_type_lower in ['dog', 'cat', 'ferret']:
        checklist_items.append(f"*   **Leash/Harness**: If applicable, for safe transport and control.")
    
    checklist_items.append(f"*   **Comfort Items**: {pet_name}'s favorite blanket, toys, and a familiar scent item to reduce stress.")
    checklist_items.append(f"*   **Identification**: Collar with up-to-date tags, microchip information, recent photo, and a description of {pet_name}.")
    checklist_items.append(f"*   **Veterinary Records**: Copies of vaccination records, medical history, and contact info for your veterinarian.")
    
    if pet_type_lower == 'cat':
        checklist_items.append(f"*   **Waste Management**: Litter box, litter, scoop, and waste bags.")
    elif pet_type_lower == 'dog':
        checklist_items.append(f"*   **Waste Management**: Waste bags and a designated potty area plan.")
    elif pet_type_lower in ['bird', 'reptile', 'fish', 'small mammal']:
        checklist_items.append(f"*   **Habitat Essentials**: Appropriate bedding, heating/lighting elements, and cleaning supplies.")

    checklist_items.append(f"*   **Emergency Contacts**: List of trusted friends/family who can assist with {pet_name} if you're unreachable.")

    actions_to_take.append(f"*   **Practice Evacuation**: Get {pet_name} used to their carrier/crate and short car rides (if applicable).")
    actions_to_take.append(f"*   **Designate Safe Space**: Identify a secure, quiet area in your home for {pet_name} during emergencies.")
    actions_to_take.append(f"*   **Buddy System**: Arrange with a neighbor or friend to check on {pet_name} if you're unreachable.")
    if pet_type_lower in ['dog', 'cat']:
        actions_to_take.append(f"*   **Training**: Ensure basic commands are reinforced for better control in stressful situations.")

    output = f"# Apocalypse Preparedness Checklist for {pet_name} ({pet_type.capitalize()})\n\n"
    output += "## Essential Supplies:\n\n"
    output += "\n".join(checklist_items)
    output += "\n\n## Actions to Take:\n\n"
    output += "\n".join(actions_to_take)
    output += "\n\nStay safe out there, and keep your pets purring/barking/chirping/hissing!"

    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate an apocalypse preparedness checklist for your pet.")
    parser.add_argument("--name", required=True, help="The name of your pet.")
    parser.add_argument("--type", required=True, help="The type of your pet (e.g., dog, cat, bird, reptile, fish, small mammal).")
    parser.add_argument("--special-needs", help="Any special medical needs or considerations for your pet.")

    args = parser.parse_args()

    checklist = generate_checklist(args.name, args.type, args.special_needs)
    print(checklist)
