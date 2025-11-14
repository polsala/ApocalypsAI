# Apocalypse Preparedness Checklist Generator

A whimsical-yet-useful utility to generate a personalized preparedness checklist for various apocalyptic scenarios. Because even in the end times, a little planning goes a long way!

## Features

*   Generates a comprehensive list of general survival items.
*   Adds scenario-specific items for popular doomsday events like `zombie` outbreaks, `meteor` impacts, or `AI uprising`s.
*   Outputs a clean Markdown checklist, ready for printing or digital use.

## Usage

To generate a checklist, you can run the `checklist_generator.py` script directly or call its `generate_checklist` function from another Python script.

```bash
python src/checklist_generator.py
```

Or, integrate it into your Python projects:

```python
from src.checklist_generator import generate_checklist

# Generate a checklist for a zombie apocalypse
zombie_checklist = generate_checklist("zombie apocalypse")
print(zombie_checklist)

# Generate a checklist for a meteor impact
meteor_checklist = generate_checklist("meteor")
print(meteor_checklist)

# Generate a general preparedness checklist
general_checklist = generate_checklist("general")
print(general_checklist)

# For an unknown or unsupported specific scenario, it will provide a general checklist with a warning
alien_checklist = generate_checklist("alien invasion")
print(alien_checklist)
```

## Example Output (for "zombie apocalypse")

```markdown
# Apocalypse Preparedness Checklist: Zombie Apocalypse

- [ ] Water (1 gallon per person per day, 3-day supply minimum)
- [ ] Non-perishable food (3-day supply minimum)
- [ ] First aid kit (with extra meds)
- [ ] Flashlight and extra batteries
- [ ] Whistle (to signal for help)
- [ ] Dust mask (to filter contaminated air)
- [ ] Wrench or pliers (to turn off utilities)
- [ ] Manual can opener
- [ ] Local maps (physical, not digital)
- [ ] Battery-powered or hand-crank radio
- [ ] Chargers and power bank for cell phones
- [ ] Cash (small bills)
- [ ] Important documents (copies in waterproof bag)
- [ ] Sleeping bag or warm blanket for each person
- [ ] Fire extinguisher
- [ ] Matches or lighter
- [ ] Multi-tool
- [ ] Personal hygiene items
- [ ] Pet food and extra water for pets
- [ ] Books, games, puzzles (for entertainment)
- [ ] Duct tape (the ultimate survival tool)
- [ ] Plastic sheeting (to create a shelter-in-place seal)
- [ ] Crowbar or blunt weapon (for 'persuasion')
- [ ] Running shoes (for quick escapes)
- [ ] Bite-proof clothing (if you can find it)
- [ ] Decoy noisemakers (to distract the 'unliving')
- [ ] A copy of 'The Zombie Survival Guide'
```
