# Apocalypse Prep Checklist Generator

## Overview

The `apocalypse-prep-checklist-generator` is a whimsical-yet-useful utility designed to help you prepare for various end-of-world scenarios. Based on your chosen apocalypse type, location, and personal skills, it generates a personalized checklist of essential tasks and items to consider for survival. Whether it's a zombie horde, a meteor strike, or an AI uprising, this tool provides a structured (and slightly tongue-in-cheek) guide to your readiness.

## Features

*   **Scenario-Specific Advice**: Tailors recommendations based on the type of apocalypse.
*   **Location-Aware Suggestions**: Adapts advice for urban, rural, or bunker environments.
*   **Skill-Based Enhancements**: Integrates your personal skills into the preparedness plan.
*   **Self-Contained**: A single Python script with no external dependencies beyond standard library.

## How to Use

1.  Navigate to the `utils/apocalypse-prep-checklist-generator/src` directory.
2.  Run the `generator.py` script with the desired arguments:

    ```bash
    python generator.py --scenario <scenario_type> --location <location_type> --skills <skill1> [<skill2> ...]
    ```

    *   `<scenario_type>`: Choose from `zombie`, `meteor`, `ai_uprising`.
    *   `<location_type>`: Choose from `urban`, `rural`, `bunker`.
    *   `<skill1> [<skill2> ...]`: Provide one or more skills from `first_aid`, `coding`, `survivalist`.

### Examples

**1. Preparing for a Zombie Apocalypse in an Urban Area with First Aid skills:**

```bash
python generator.py --scenario zombie --location urban --skills first_aid
```

**2. Preparing for an AI Uprising in a Rural Area with Coding and Survivalist skills:**

```bash
python generator.py --scenario ai_uprising --location rural --skills coding survivalist
```

## Example Output

```
--- Apocalypse Preparedness Checklist ---

Scenario: AI Uprising
Location: Rural
Skills: Coding, Survivalist

[General Preparedness]
- Secure a reliable, off-grid power source.
- Stockpile non-perishable food and clean water for at least 6 months.
- Establish a robust communication plan with trusted allies (analog preferred).
- Maintain physical fitness and mental resilience.

[AI Uprising Specifics]
- Construct a Faraday cage for sensitive electronics.
- Develop or acquire EMP devices to disable rogue AI systems.
- Prioritize analog tools and information sources.
- Secure and encrypt critical data, prepare for offline operation.
- Learn basic social engineering to bypass AI-controlled systems.

[Rural Location Specifics]
- Identify local water sources and purification methods.
- Learn foraging, hunting, and trapping techniques.
- Master basic shelter construction from natural materials.
- Establish defensive perimeters and escape routes.

[Coding Skill Enhancements]
- Develop offline tools for data analysis and communication.
- Practice reverse-engineering AI protocols (if safe).
- Secure your own digital footprint and create ghost identities.

[Survivalist Skill Enhancements]
- Refine advanced navigation techniques (map, compass, stars).
- Practice advanced trap setting and wilderness survival.
- Master fire starting in adverse conditions.

--- End of Checklist ---
```
