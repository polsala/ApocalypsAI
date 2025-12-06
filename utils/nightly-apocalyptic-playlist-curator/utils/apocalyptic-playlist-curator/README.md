# Apocalyptic Playlist Curator

## Overview
In the desolate quiet of the post-apocalypse, music is more than just sound – it's a lifeline. The Apocalyptic Playlist Curator is a simple, yet essential, utility designed to help survivors organize their precious audio archives into thematic playlists. Whether you're hunkered down in a bunker, scavenging for supplies, or just need a moment of quiet reflection, this tool ensures you have the perfect soundtrack.

It scans a specified directory for audio files, identifies keywords in their filenames, and then generates `.m3u` playlist files, ready for your preferred media player.

## Features
*   **Keyword-based Categorization**: Automatically groups songs into playlists based on predefined keywords found in their filenames (e.g., 'bunker', 'scavenge', 'epic', 'chill').
*   **Common Audio Support**: Recognizes `.mp3`, `.wav`, `.ogg`, and `.flac` files.
*   **`.m3u` Output**: Generates standard `.m3u` playlist files, compatible with most audio players.
*   **Self-Contained**: No external dependencies beyond Python's standard library.

## Usage

To run the curator, navigate to the `apocalyptic-playlist-curator` directory and execute the `curator.py` script with your music source directory and desired output directory:

```bash
python src/curator.py <music_source_directory> <output_playlist_directory>
```

**Example:**

```bash
python src/curator.py /home/survivor/music_stash /home/survivor/playlists
```

This will scan `/home/survivor/music_stash` for audio files, categorize them, and save the generated `.m3u` files into `/home/survivor/playlists`.

## Keyword Mappings
The curator uses the following default keyword-to-playlist mappings. If a filename contains one of these keywords (case-insensitive), it will be added to the corresponding playlist.

| Keyword   | Playlist Name          |
| :-------- | :--------------------- |
| `bunker`  | Bunker_Beats           |
| `scavenge`| Scavenging_Soundtrack  |
| `epic`    | Epic_Anthems           |
| `chill`   | Chill_Out_Zone         |
| `somber`  | Somber_Reflections     |
| `hope`    | Glimmers_of_Hope       |
| `radio`   | Static_Radio_Hits      |

Files not matching any keyword will not be added to any themed playlist, but will still be processed if they are valid audio files.

## Development

Feel free to extend the keyword mappings in `src/curator.py` to suit your specific post-apocalyptic mood swings!
