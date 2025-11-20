# Scavenger Manifest Generator

## Overview

The Scavenger Manifest Generator is a crucial tool for any survivor in the post-apocalyptic wasteland. It helps you plan your daily scavenging runs by generating a prioritized checklist of items to look for, based on your current needs, your willingness to take risks, and the precious hours you have available.

No more aimless wandering! With this manifest, you'll know exactly what to seek, maximizing your chances of survival and resource acquisition.

## Usage

Run the script from your terminal:

```bash
python src/manifest_generator.py --food 2 --water 1 --parts 1 --risk medium --hours 4
```

### Arguments:

*   `--food <int>`: Desired units of food.
*   `--water <int>`: Desired units of water.
*   `--parts <int>`: Desired units of repair/crafting parts.
*   `--medical <int>`: Desired units of medical supplies.
*   `--tools <int>`: Desired units of tools.
*   `--morale <int>`: Desired units of morale boosters.
*   `--risk <low|medium|high>`: Your tolerance for danger. Affects which areas/items are suggested.
*   `--hours <float>`: The maximum number of hours you can spend scavenging.

## Example Output

```
--- Scavenging Manifest for 2023-10-27 ---

Prioritized Needs:
- Food: 2 units
- Water: 1 unit
- Parts: 1 unit

Risk Tolerance: Medium
Time Available: 4.0 hours

--- Your Mission Checklist ---

1.  Canned Goods (Food) - Priority: High, Risk: Low, Time: 0.6h
2.  Purification Tablet (Water) - Priority: High, Risk: Low, Time: 0.2h
3.  Scrap Metal (Parts) - Priority: High, Risk: Low, Time: 0.3h
4.  Tool Kit (Tools) - Priority: High, Risk: Medium, Time: 1.2h

Total Estimated Time: 2.3 hours

Good luck, survivor! May your hauls be plentiful and your encounters minimal.
```

## Development

To run tests:

```bash
python -m unittest tests/test_manifest_generator.py
```
