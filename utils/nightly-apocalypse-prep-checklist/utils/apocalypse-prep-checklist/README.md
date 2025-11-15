# Apocalypse Prep Checklist Generator

## Description

This utility generates a markdown checklist of essential items and actions for surviving various hypothetical apocalypse scenarios. Whether you're bracing for a zombie horde, an AI uprising, or a devastating solar flare, this tool provides a whimsical-yet-structured guide to your preparations.

It's designed to be self-contained and run offline, providing instant, deterministic advice for your impending doom.

## Usage

To generate a checklist, run the `prep_kit_generator.py` script with the desired scenario as an argument:

```bash
python src/prep_kit_generator.py <scenario>
```

### Available Scenarios:

*   `zombie-apocalypse`
*   `ai-uprising`
*   `solar-flare`

If an unknown or unsupported scenario is provided, a generic basic survival checklist will be generated.

## Example

```bash
python src/prep_kit_generator.py zombie-apocalypse
```

**Output:**

```markdown
# Zombie Apocalypse Prep Checklist

- [ ] Crowbar (for brain-smashing and door-opening)
- [ ] First-aid kit (for bites and scrapes)
- [ ] Non-perishable food (canned goods, MREs)
- [ ] Water purification tablets
- [ ] Map of local area (avoiding known zombie hotspots)
- [ ] Walkie-talkie (for silent communication)
- [ ] Duct tape (for everything)
- [ ] A good pair of running shoes
- [ ] "Zombieland" survival guide (for inspiration)
```
