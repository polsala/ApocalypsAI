# Nightly Wasteland Waypoint Tracker

## 🗺️ Navigate the Digital Rubble with Precision!

In the ever-shifting landscape of post-apocalyptic development, it's easy to lose track of crucial resources. The `Nightly Wasteland Waypoint Tracker` is your trusty companion, a simple command-line utility to help you log and retrieve important file paths, URLs, and notes – your digital waypoints.

Never again will you wander aimlessly searching for that obscure config file, the forgotten API endpoint, or the cryptic note from a bygone era. Mark your waypoints, tag them for easy retrieval, and keep your development journey on track!

## ✨ Features

*   **Add Waypoint**: Log a new path, URL, or note with a name, description, and tags.
*   **List Waypoints**: View all your recorded waypoints.
*   **Search Waypoints**: Quickly find waypoints by name, target, description, or tags.
*   **Delete Waypoint**: Remove obsolete waypoints.
*   **Persistent Storage**: All waypoints are saved to a local `waypoints.json` file.

## 🚀 Usage

To run the tracker, navigate to the `src` directory and execute `tracker.py` with the desired commands.

### Add a new waypoint

```bash
python src/tracker.py add --name "Project X Config" --target "/home/user/projects/x/config.yaml" --tags "config,yaml,project-x" --description "Main configuration file for Project X, crucial for deployment."
python src/tracker.py add --name "ApocalypsAI Docs" --target "https://github.com/polsala/ApocalypsAI/blob/main/AGENTS.md" --tags "docs,agent,github" --description "The sacred contract for all ApocalypsAI agents."
python src/tracker.py add --name "Scavenged Data Cache" --target "./data/cache/temp_loot.json" --tags "data,temp,loot" --description "Temporary storage for recently scavenged data, needs processing."
```

### List all waypoints

```bash
python src/tracker.py list
```

### Search for waypoints

Search by any part of the name, target, description, or tags.

```bash
python src/tracker.py search "config"
python src/tracker.py search "agent"
python src/tracker.py search "temp_loot"
```

### Delete a waypoint

First, `list` your waypoints to find the `ID` of the one you want to delete.

```bash
python src/tracker.py delete --id <waypoint_id>
# Example: python src/tracker.py delete --id 1234567890
```

## 🛠️ Development

The utility is written in Python 3.11 and stores its data in a simple JSON file named `waypoints.json` in the same directory as the script. Feel free to inspect or modify it to suit your specific wasteland needs.
