# Apocalypse Prep Checklist Generator

## Overview

Prepare for the inevitable with the `apocalypse-prep-checklist` utility! This tool generates a customized survival checklist based on your chosen apocalyptic scenario, current location, and available resources. Whether it's a zombie horde, a meteor strike, an AI uprising, or a solar flare, get your ducks in a row (or your canned goods in the bunker).

It's designed to be both whimsical and genuinely useful, prompting thought about practical survival needs in a fun, self-contained way.

## Usage

To generate a checklist, run the `checklist_generator.py` script with the following arguments:

```bash
python src/checklist_generator.py \
  --scenario <scenario_type> \
  --location <location_type> \
  --resources <resource_level>
```

### Arguments:

*   `--scenario`: The type of apocalypse. Choose from: `zombie_outbreak`, `meteor_strike`, `ai_uprising`, `solar_flare`.
*   `--location`: Your current environment. Choose from: `urban`, `rural`, `suburban`.
*   `--resources`: Your current resource level. Choose from: `minimal`, `moderate`, `abundant`.

### Example:

```bash
python src/checklist_generator.py --scenario zombie_outbreak --location urban --resources moderate
```

This will output a Markdown-formatted checklist to your console, which you can then save or print.

## Example Output (for `zombie_outbreak`, `urban`, `moderate`)

```markdown
# Apocalypse Survival Checklist: Zombie Outbreak (Urban, Moderate Resources)

## Immediate Actions:

*   Secure your dwelling: Barricade doors and windows with heavy furniture.
*   Gather essential supplies: Water (3 days supply per person), non-perishable food, first-aid kit.
*   Establish communication plan: Designate a rally point and check-in times with family/friends.
*   Stay informed: Monitor emergency broadcasts (if available).
*   Ensure all entry points are sealed against the undead.
*   Prepare blunt and bladed melee weapons; firearms if available and trained.

## Mid-Term Preparedness:

*   Scavenge for resources: Prioritize water filters, medical supplies, durable tools.
*   Fortify your position: Reinforce entry points, create escape routes.
*   Learn basic self-defense: Improvise weapons, practice evasion tactics.
*   Conserve power: Limit use of electronics, rely on manual tools.
*   Practice silent movement and evasion techniques.
*   Learn basic zombie anatomy (headshots are key!).

## Long-Term Survival:

*   Seek a safer location: Consider moving to higher ground or less populated areas.
*   Cultivate food sources: Start a small garden if feasible, learn foraging.
*   Form alliances: Connect with other survivors for mutual protection and resource sharing.
*   Maintain morale: Find ways to stay positive and mentally resilient.
*   Establish a secure, defensible perimeter.
*   Develop a system for waste disposal to avoid attracting attention.

## Resource Adjustments (Moderate):

*   You have some existing supplies; focus on replenishing and diversifying.
*   Consider investing in a solar charger for small electronics.
*   Prioritize durable goods over consumables during scavenging.

## Location Specifics (Urban):

*   High population density means more immediate threats but also more potential resources.
*   Focus on stealth and avoiding main thoroughfares.
*   Utilize rooftops and elevated structures for observation and movement.

---

*Stay vigilant, stay safe, and may your aim be true!*
```

## Development

This utility is written in Python 3.11 and is self-contained. It uses only standard library modules.

## Testing

Tests are located in the `tests/` directory and can be run using `pytest` (install with `pip install pytest`).

```bash
pytest tests/
```
