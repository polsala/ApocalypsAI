import argparse
import sys

def get_checklist(scenario: str) -> list[str]:
    """Returns a preparedness checklist for a given scenario."""
    scenarios = {
        "zombie": [
            "Secure a safe location (high ground, defensible structure)",
            "Stockpile non-perishable food and water (30-day supply minimum)",
            "Assemble a comprehensive first-aid kit",
            "Acquire a blunt melee weapon (crowbar, baseball bat)",
            "Plan multiple escape routes and rendezvous points",
            "Ensure reliable communication (walkie-talkies, signal flares)",
            "Gather sturdy clothing and footwear",
            "Learn basic survival skills (fire starting, knot tying)"
        ],
        "ai-uprising": [
            "Build an EMP-proof Faraday cage for essential electronics",
            "Back up critical data to offline, non-networked storage",
            "Stock manual tools and mechanical devices (no smart tech)",
            "Learn basic mechanics and electronics repair",
            "Establish analog communication methods (shortwave radio, signal flags)",
            "Disable all smart home devices and IoT gadgets",
            "Develop a code of conduct for human-AI interaction (if unavoidable)",
            "Practice navigating without GPS or digital maps"
        ],
        "meteor-strike": [
            "Identify or construct an underground shelter",
            "Stock long-term food and water purification supplies",
            "Acquire radiation suits and Geiger counter (if impact is radioactive)",
            "Install robust air filtration and ventilation systems",
            "Secure emergency power sources (solar, hand-crank, geothermal)",
            "Establish long-range communication array (satellite phone, ham radio)",
            "Gather seeds for post-impact agriculture",
            "Develop a plan for debris removal and structural reinforcement"
        ],
        "solar-flare": [
            "Build an EMP-proof Faraday cage for essential electronics",
            "Stock manual tools and mechanical devices (no smart tech)",
            "Secure backup power sources (solar, hand-crank, generator - non-grid dependent)",
            "Learn basic mechanics and electronics repair",
            "Establish analog communication methods (shortwave radio, signal flags)",
            "Protect sensitive electronics by unplugging them during a flare warning",
            "Have physical maps and compass for navigation",
            "Stockpile cash and barter items"
        ],
        "general": [
            "Stockpile non-perishable food and water (72-hour supply minimum)",
            "Assemble a comprehensive first-aid kit",
            "Gather important documents (IDs, insurance, deeds) in a waterproof bag",
            "Prepare an emergency cash stash and small denominations",
            "Pack a multi-tool, flashlight, and extra batteries",
            "Ensure a reliable communication device (fully charged phone, power bank)",
            "Have a 'go-bag' with essential clothing and personal hygiene items",
            "Know your local emergency services and evacuation routes"
        ]
    }
    return scenarios.get(scenario.lower(), [])

def main():
    parser = argparse.ArgumentParser(
        description="Generate an apocalypse preparedness checklist."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        required=True,
        help="The apocalypse scenario (e.g., zombie, ai-uprising, meteor-strike, solar-flare, general)"
    )
    args = parser.parse_args()

    checklist = get_checklist(args.scenario)

    if not checklist:
        print(f"Error: Unknown scenario '{args.scenario}'. Please choose from: zombie, ai-uprising, meteor-strike, solar-flare, general.")
        sys.exit(1)

    print(f"--- Apocalypse Prep Checklist: {args.scenario.replace('-', ' ').title()} ---")
    for i, item in enumerate(checklist, 1):
        print(f"{i}. [ ] {item}")
    print("--------------------------------------------------")

if __name__ == "__main__":
    main()
