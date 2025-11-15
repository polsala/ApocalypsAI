import argparse
import sys

def generate_checklist(scenario: str, location: str, skills: list[str]) -> str:
    """
    Generates a personalized apocalypse preparedness checklist.
    """
    checklist_items = []

    # General Preparedness
    checklist_items.append("[General Preparedness]")
    checklist_items.append("- Secure a reliable, off-grid power source.")
    checklist_items.append("- Stockpile non-perishable food and clean water for at least 6 months.")
    checklist_items.append("- Establish a robust communication plan with trusted allies (analog preferred).")
    checklist_items.append("- Maintain physical fitness and mental resilience.")
    checklist_items.append("")

    # Scenario-Specific Preparedness
    checklist_items.append(f"[{scenario.replace('_', ' ').title()} Specifics]")
    if scenario == "zombie":
        checklist_items.append("- Barricade entry points and secure your perimeter.")
        checklist_items.append("- Acquire blunt weapons for close-quarters combat (and practice).")
        checklist_items.append("- Master the art of the headshot (practice on mannequins, not neighbors).")
        checklist_items.append("- Secure long-term, non-perishable food sources away from population centers.")
    elif scenario == "meteor":
        checklist_items.append("- Identify or construct a sturdy underground shelter.")
        checklist_items.append("- Stockpile water purification tablets and filters.")
        checklist_items.append("- Prepare for long-term isolation and radiation fallout.")
        checklist_items.append("- Establish emergency communication protocols (shortwave radio, signal mirrors).")
    elif scenario == "ai_uprising":
        checklist_items.append("- Construct a Faraday cage for sensitive electronics.")
        checklist_items.append("- Develop or acquire EMP devices to disable rogue AI systems.")
        checklist_items.append("- Prioritize analog tools and information sources.")
        checklist_items.append("- Secure and encrypt critical data, prepare for offline operation.")
        checklist_items.append("- Learn basic social engineering to bypass AI-controlled systems.")
    checklist_items.append("")

    # Location-Specific Preparedness
    checklist_items.append(f"[{location.title()} Location Specifics]")
    if location == "urban":
        checklist_items.append("- Map out multiple escape routes from your current location.")
        checklist_items.append("- Practice stealth and urban evasion techniques.")
        checklist_items.append("- Identify hidden caches of resources (abandoned stores, utility tunnels).")
        checklist_items.append("- Understand public transport systems for rapid relocation.")
    elif location == "rural":
        checklist_items.append("- Identify local water sources and purification methods.")
        checklist_items.append("- Learn foraging, hunting, and trapping techniques.")
        checklist_items.append("- Master basic shelter construction from natural materials.")
        checklist_items.append("- Establish defensive perimeters and escape routes.")
    elif location == "bunker":
        checklist_items.append("- Ensure air filtration and ventilation systems are operational.")
        checklist_items.append("- Manage waste and sanitation effectively within confined spaces.")
        checklist_items.append("- Develop a robust power generation and storage system.")
        checklist_items.append("- Cultivate psychological resilience for long-term isolation.")
    checklist_items.append("")

    # Skill-Based Enhancements
    if skills:
        for skill in skills:
            checklist_items.append(f"[{skill.replace('_', ' ').title()} Skill Enhancements]")
            if skill == "first_aid":
                checklist_items.append("- Assemble a comprehensive medical kit and learn advanced wound care.")
                checklist_items.append("- Practice basic surgical procedures (on non-living subjects, ideally).")
                checklist_items.append("- Understand disease prevention and hygiene in primitive conditions.")
            elif skill == "coding":
                checklist_items.append("- Develop offline tools for data analysis and communication.")
                checklist_items.append("- Practice reverse-engineering AI protocols (if safe and ethical).")
                checklist_items.append("- Secure your own digital footprint and create ghost identities.")
                checklist_items.append("- Learn to repurpose defunct electronics for new uses.")
            elif skill == "survivalist":
                checklist_items.append("- Refine advanced navigation techniques (map, compass, stars).")
                checklist_items.append("- Practice advanced trap setting and wilderness survival.")
                checklist_items.append("- Master fire starting in adverse conditions.")
                checklist_items.append("- Learn to identify edible and medicinal plants.")
            checklist_items.append("")

    return "\n".join([
        "--- Apocalypse Preparedness Checklist ---",
        f"Scenario: {scenario.replace('_', ' ').title()}",
        f"Location: {location.title()}",
        f"Skills: {', '.join([s.replace('_', ' ').title() for s in skills]) if skills else 'None'}",
        "",
        *checklist_items,
        "--- End of Checklist ---"
    ])

def main():
    parser = argparse.ArgumentParser(
        description="Generate a personalized apocalypse preparedness checklist."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        choices=["zombie", "meteor", "ai_uprising"],
        required=True,
        help="Type of apocalypse scenario."
    )
    parser.add_argument(
        "--location",
        type=str,
        choices=["urban", "rural", "bunker"],
        required=True,
        help="Your current or planned location type."
    )
    parser.add_argument(
        "--skills",
        nargs="*",
        type=str,
        choices=["first_aid", "coding", "survivalist"],
        default=[],
        help="Your relevant skills (can provide multiple)."
    )

    args = parser.parse_args()

    checklist = generate_checklist(args.scenario, args.location, args.skills)
    print(checklist)

if __name__ == "__main__":
    main()
