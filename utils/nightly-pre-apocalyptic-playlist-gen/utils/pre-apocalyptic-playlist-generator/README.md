# Pre-Apocalyptic Playlist Generator

## 🎶 Set the Mood for the End Times 🎶

This utility helps you curate the perfect soundtrack for any pre-apocalyptic scenario. Whether you're fortifying your bunker, contemplating the vastness of the void, or just need some background music for your last stand, the Pre-Apocalyptic Playlist Generator has you covered. It draws from a local `music_manifest.json` to create mood-specific playlists.

## Usage

Run the script with your desired mood and the number of songs you want:

```bash
python src/playlist_generator.py --mood dystopian --count 5
```

### Arguments:
*   `--mood <mood>`: The desired mood for the playlist (e.g., `calm`, `energetic`, `dystopian`, `hopeful`). Must match a key in `music_manifest.json`.
*   `--count <int>`: The number of songs to include in the playlist. Defaults to 5.
*   `--manifest <path>`: Optional. Path to the music manifest JSON file. Defaults to `src/music_manifest.json`.

## Configuration

The utility relies on `src/music_manifest.json` to define available songs and their associated moods. You can customize this file to include your own favorite tracks.

### `music_manifest.json` Structure:

```json
{
  "calm": [
    {"title": "Weightless", "artist": "Marconi Union"},
    {"title": "Adagio for Strings", "artist": "Samuel Barber"}
  ],
  "energetic": [
    {"title": "Thunderstruck", "artist": "AC/DC"},
    {"title": "Sabotage", "artist": "Beastie Boys"}
  ],
  "dystopian": [
    {"title": "Mad World", "artist": "Tears for Fears"},
    {"title": "Hurt", "artist": "Johnny Cash"}
  ],
  "hopeful": [
    {"title": "What a Wonderful World", "artist": "Louis Armstrong"}
  ]
}
```

## Example Output

```
--- Pre-Apocalyptic Playlist (dystopian) ---
1. Mad World by Tears for Fears
2. Hurt by Johnny Cash
3. The Sound of Silence by Simon & Garfunkel
4. Where Is My Mind? by Pixies
5. Creep by Radiohead
-------------------------------------------
```
