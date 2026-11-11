# Nightly Apocalypse Tunes Generator

Curate the perfect soundtrack for the end of days! This utility helps you generate a mood-specific playlist from your personal song collection, ensuring you have the right tunes whether you're scavenging, contemplating the void, or preparing for a raid.

## Features

*   **Mood-Based Filtering**: Select songs based on predefined or custom moods.
*   **Flexible Input**: Uses a simple JSON file for your song library.
*   **Thematic Output**: Presents your playlist in a fitting post-apocalyptic style.

## Installation

1.  Navigate to the `nightly-apocalypse-tunes` directory.
2.  Install dependencies:
    ```bash
    npm install
    ```

## Usage

1.  **Prepare your song library**: Create a JSON file (e.g., `songs.json`) with your music data. Each song should have at least a `title` and `artist`. You can also add `tags` to help with mood filtering.

    ```json
    [
      {
        "title": "Wasteland Wanderer",
        "artist": "The Rad-Scorpions",
        "tags": ["exploration", "somber", "journey"]
      },
      {
        "title": "Raid on Sector 7",
        "artist": "Mutant Mayhem",
        "tags": ["action", "upbeat", "combat"]
      },
      {
        "title": "Echoes of the Old World",
        "artist": "The Silent Survivors",
        "tags": ["contemplation", "melancholy"]
      },
      {
        "title": "Scavenger's Anthem",
        "artist": "Dusty Road Crew",
        "tags": ["exploration", "upbeat"]
      }
    ]
    ```

2.  **Run the generator**: The `--file` and `--mood` arguments expect single-word values. If your file path or mood contains spaces, you may need to adjust your input or use a symbolic link for paths.
    ```bash
    node src/index.js --file ./songs.json --mood exploration
    ```

    Or using the `npm start` script:
    ```bash
    npm start -- --file ./songs.json --mood contemplation
    ```

### Arguments

*   `--file <path>`: **(Required)** Path to your JSON song library file.
*   `--mood <mood_name>`: **(Required)** The desired mood for your playlist.
    *   Supported moods (and their associated tags):
        *   `exploration`: `exploration`, `journey`, `discovery`, `wander`
        *   `contemplation`: `contemplation`, `melancholy`, `somber`, `reflection`
        *   `action`: `action`, `combat`, `upbeat`, `raid`, `survival`
        *   `chill`: `chill`, `relax`, `calm`, `peace`
        *   Any other mood will attempt to match its name as a tag.

## Example Output

```
--- Nightly Apocalypse Tunes: Exploration Playlist ---

1. Wasteland Wanderer by The Rad-Scorpions
2. Scavenger's Anthem by Dusty Road Crew

----------------------------------------------------
```
