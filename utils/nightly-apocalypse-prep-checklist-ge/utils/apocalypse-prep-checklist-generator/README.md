# Apocalypse Prep Checklist Generator

## Overview

Feeling a bit unprepared for the inevitable? The `apocalypse-prep-checklist-generator` is here to help! This utility provides a tailored survival checklist based on various doomsday scenarios, from the classic zombie horde to a rogue AI uprising. It's designed to be both genuinely useful for basic preparedness and a source of lighthearted (or darkhearted) amusement.

## Features

*   **Scenario-based Checklists**: Get specific advice for different types of apocalypses.
*   **Whimsical & Practical**: A blend of serious survival tips and humorous, scenario-specific suggestions.
*   **Self-contained**: A single Python script, easy to run anywhere.

## Usage

To generate a checklist, run the script with your desired scenario:

```bash
python src/generator.py --scenario <scenario_name>
```

### Available Scenarios:

*   `zombie`: For when the undead rise.
*   `meteor`: When the sky falls.
*   `ai-uprising`: When your smart devices get *too* smart.
*   `solar-flare`: When the sun decides to get spicy.
*   `default`: General preparedness for any unforeseen event.

If no scenario is provided or an unknown scenario is given, the `default` checklist will be used.

### Example:

```bash
python src/generator.py --scenario zombie
```

**Output for `zombie` scenario:**

```
--- Apocalypse Prep Checklist: Zombie Uprising ---

1. Secure all entry points (doors, windows, vents). Seriously.
2. Stockpile non-perishable food and water (at least 3-day supply per person).
3. Learn basic first aid and wound care (zombie bites are messy).
4. Identify a safe, defensible location (high ground, limited access).
5. Acquire blunt force trauma weapons (crowbar, baseball bat) and practice headshots (on targets, please!).
6. Have a bug-out bag ready with essentials for quick evacuation.
7. Establish a communication plan with your survival group (no cell service).
8. Practice stealth and evasion techniques.
9. Remember: Cardio is key.

Stay vigilant, survivor!
```
