import json
import random
import argparse
import sys
import os

def load_music_manifest(manifest_path):
    """Loads the music manifest from a JSON file."""
    if not os.path.exists(manifest_path):
        print(f"Error: Music manifest not found at '{manifest_path}'.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{manifest_path}'.", file=sys.stderr)
        sys.exit(1)

def generate_playlist(mood, count, manifest_data):
    """Generates a playlist based on mood and count from the manifest data."""
    if mood not in manifest_data:
        print(f"Error: Mood '{mood}' not found in the music manifest.", file=sys.stderr)
        sys.exit(1)

    available_songs = manifest_data[mood]

    if not available_songs:
        print(f"Warning: No songs found for mood '{mood}'. Returning an empty playlist.", file=sys.stderr)
        return []

    if count <= 0:
        print(f"Warning: Requested {count} songs. Returning an empty playlist.", file=sys.stderr)
        return []

    if count > len(available_songs):
        print(f"Warning: Requested {count} songs, but only {len(available_songs)} available for mood '{mood}'. Returning all available songs.", file=sys.stderr)
        return random.sample(available_songs, len(available_songs))
    else:
        return random.sample(available_songs, count)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a pre-apocalyptic music playlist based on mood."
    )
    parser.add_argument(
        "--mood", 
        type=str, 
        required=True, 
        help="The desired mood for the playlist (e.g., calm, energetic, dystopian)"
    )
    parser.add_argument(
        "--count", 
        type=int, 
        default=5, 
        help="The number of songs to include in the playlist (default: 5)"
    )
    parser.add_argument(
        "--manifest", 
        type=str, 
        default=os.path.join(os.path.dirname(__file__), "music_manifest.json"), 
        help="Path to the music manifest JSON file"
    )

    args = parser.parse_args()

    manifest_data = load_music_manifest(args.manifest)
    playlist = generate_playlist(args.mood, args.count, manifest_data)

    if playlist:
        print(f"\n--- Pre-Apocalyptic Playlist ({args.mood}) ---")
        for i, song in enumerate(playlist):
            print(f"{i+1}. {song['title']} by {song['artist']}")
        print("-------------------------------------------")
    else:
        # This branch is reached if playlist is empty due to no songs for mood, or count <= 0
        if args.mood in manifest_data and manifest_data[args.mood] and args.count > 0:
            # This case should ideally not be reached if warnings are printed correctly
            pass # Warning already printed by generate_playlist
        elif args.mood in manifest_data and not manifest_data[args.mood]:
            # Warning already printed by generate_playlist
            pass
        elif args.count <= 0:
            # Warning already printed by generate_playlist
            pass
        else:
            # Fallback for unexpected empty playlist
            print(f"No songs generated for mood '{args.mood}'.")

if __name__ == "__main__":
    main()
