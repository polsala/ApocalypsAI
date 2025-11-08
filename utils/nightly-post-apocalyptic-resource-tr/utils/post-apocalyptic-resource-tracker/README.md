# Post-Apocalyptic Resource Tracker

## Overview

In the grim darkness of the post-apocalypse, every can of beans, every drop of purified water, and every bullet counts. But more importantly, so does your sanity! The `post-apocalyptic-resource-tracker` is a simple, self-contained command-line utility designed to help your survivor group keep tabs on your dwindling (or occasionally replenished) vital resources.

It's perfect for managing your inventory in a world where spreadsheets are a luxury and a pen and paper might attract unwanted attention.

## Features

*   **Add Resources**: Easily log new supplies found during scavenging runs.
*   **Consume Resources**: Deduct items used for survival or defense.
*   **List Resources**: Get a quick overview of your current stock.
*   **Persistence**: All data is saved to a local `resources.json` file, so your inventory survives reboots (and perhaps even a zombie horde).

## Installation

This utility is self-contained. Simply navigate to the `utils/post-apocalyptic-resource-tracker/` directory.

## Usage

Run the `tracker.py` script with various commands:

### Add Resources

To add a resource or increase its quantity:

```bash
python src/tracker.py add <resource_name> <quantity>
# Example: Found 5 cans of beans
python src/tracker.py add food_beans 5
# Example: Found a new supply of water
python src/tracker.py add water_purified 10
# Example: Your medic managed to boost morale!
python src/tracker.py add sanity 1
```

### Consume Resources

To consume a resource or decrease its quantity:

```bash
python src/tracker.py consume <resource_name> <quantity>
# Example: Ate 1 can of beans
python src/tracker.py consume food_beans 1
# Example: Used 3 bullets defending the perimeter
python src/tracker.py consume ammo_9mm 3
# Example: Lost 2 sanity points after seeing *that* thing
python src/tracker.py consume sanity 2
```

### List Resources

To see all current resources and their quantities:

```bash
python src/tracker.py list
```

## Example Workflow

```bash
# Initial setup (or first run)
python src/tracker.py add food_rations 10
python src/tracker.py add water_bottles 20
python src/tracker.py add ammo_shotgun 5
python src/tracker.py add sanity 100

# Check inventory
python src/tracker.py list
# Output:
# Current Resources:
#   food_rations: 10
#   water_bottles: 20
#   ammo_shotgun: 5
#   sanity: 100

# Consume some resources
python src/tracker.py consume food_rations 2
python src/tracker.py consume water_bottles 5
python src/tracker.py consume sanity 10

# Check again
python src/tracker.py list
# Output:
# Current Resources:
#   food_rations: 8
#   water_bottles: 15
#   ammo_shotgun: 5
#   sanity: 90

# Try to consume more than available (ammo)
python src/tracker.py consume ammo_shotgun 10
# Output:
# Consumed 5 of ammo_shotgun. Remaining: 0. (Note: You only had 5)

# Check again
python src/tracker.py list
# Output:
# Current Resources:
#   food_rations: 8
#   water_bottles: 15
#   ammo_shotgun: 0
#   sanity: 90
```
