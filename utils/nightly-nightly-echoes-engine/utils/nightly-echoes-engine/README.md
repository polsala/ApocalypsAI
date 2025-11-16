# Nightly Echoes Engine

## 🎶 Your Post-Apocalyptic Playlist Curator 🎶

In the quiet hum of the bunker, or amidst the eerie silence of the wasteland, music is more than just sound – it's a lifeline. The Nightly Echoes Engine is here to help you organize your precious audio archives into mood-specific playlists, ensuring you always have the perfect soundtrack for scavenging, strategizing, or simply surviving.

This utility scans a specified directory for audio files and intelligently categorizes them into playlists based on keywords found in their filenames or parent folder names. Whether you need 'Action & Adventure' for a daring supply run or 'Chill & Relax' for a moment of respite, the Echoes Engine has you covered.

## Features

*   **Intelligent Categorization**: Automatically groups tracks into categories like 'Chill & Relax', 'Action & Adventure', 'Focus & Productivity', and 'Broadcasts & Signals'.
*   **M3U Playlist Generation**: Creates standard `.m3u` playlist files, compatible with most media players.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.
*   **Whimsical & Useful**: Brings order to your audio chaos in the most dire of times.

## Usage

To run the Nightly Echoes Engine, navigate to its directory and execute the `echoes_engine.py` script with the path to your music library and an optional output directory for the playlists:

```bash
python src/echoes_engine.py --music-dir /path/to/your/music --output-dir /path/to/playlists
```

**Arguments:**

*   `--music-dir` (required): The root directory containing your audio files.
*   `--output-dir` (optional): The directory where generated `.m3u` playlists will be saved. If not provided, playlists will be saved in a `playlists/` subdirectory within the utility's own folder.

## Example

Given a `music/` directory structure like this:

```
music/
├── ambient_tunes/
│   └── calm_waters.mp3
│   └── deep_sleep.ogg
├── battle_anthems/
│   └── epic_clash.wav
│   └── run_for_your_life.mp3
├── focus_tracks/
│   └── coding_flow.mp3
├── old_radio_broadcast.mp3
└── unknown_track.mp3
```

Running the engine will generate `m3u` files such as:

*   `Chill_and_Relax.m3u` (containing `calm_waters.mp3`, `deep_sleep.ogg`)
*   `Action_and_Adventure.m3u` (containing `epic_clash.wav`, `run_for_your_life.mp3`)
*   `Focus_and_Productivity.m3u` (containing `coding_flow.mp3`)
*   `Broadcasts_and_Signals.m3u` (containing `old_radio_broadcast.mp3`)
*   `Miscellaneous_Echoes.m3u` (containing `unknown_track.mp3`)

## Development

Tests are located in the `tests/` directory and can be run using `pytest` or `python -m unittest`.

```bash
python -m unittest tests/test_echoes_engine.py
```
