# Apocalypse Prep Checklist Generator

Prepare for the inevitable with a touch of whimsy! This utility helps you generate a personalized preparedness checklist for various apocalyptic scenarios, tailored to your location and the size of your survival party.

## Features

*   **Scenario-Based**: Choose from classic doomsday scenarios like 'Zombie Outbreak', 'Nuclear Winter', or even 'AI Uprising'.
*   **Location-Aware**: Get recommendations specific to urban or rural environments.
*   **Group-Adjusted**: Scale your supplies based on how many survivors you're planning for.
*   **Extensible**: Easily add new scenarios and items by modifying the `data/scenarios.json` file.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are strictly required beyond standard library modules.

1.  Navigate to the `utils/apocalypse-prep-checklist/` directory.
2.  (Optional, but recommended) Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

## Usage

Run the `checklist_generator.py` script from the `src/` directory:

```bash
python3 src/checklist_generator.py
```

The script will prompt you for:

1.  **Apocalypse Scenario**: Choose from a list (e.g., `zombie`, `nuclear`, `ai`).
2.  **Location Type**: `urban` or `rural`.
3.  **Number of People**: An integer representing your survival group size.

It will then print your personalized, categorized checklist to the console.

## Example Output

```
--- Your Apocalypse Preparedness Checklist (AI Uprising, Urban, 3 People) ---

General Essentials:
- Batteries (various sizes)
- Cash (small denominations)
- Duct tape
- Fire starter
- First aid manual
- Flashlight
- Important documents (waterproof copies)
- Multi-tool
- Rope
- Whistle

Scenario-Specific:
- Analog maps
- EMP device (theoretical)
- Faraday cage (for electronics)
- Non-digital communication methods

Location-Specific:
- Bolt cutters
- Disguise kit
- EMP grenades
- Knowledge of server farms

Group-Specific:
- Decoy electronics
- Encrypted walkie-talkies
- Team communication protocols

--------------------------------------------------------------------------------
```

## Extending Scenarios

The `data/scenarios.json` file defines all available scenarios and items. You can add new scenarios, modify existing ones, or introduce new general items by editing this JSON file. Ensure the structure remains valid JSON.
