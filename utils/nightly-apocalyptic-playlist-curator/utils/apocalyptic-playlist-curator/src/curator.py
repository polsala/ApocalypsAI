import os
import argparse

def generate_playlists(music_dir, output_dir):
    """
    Scans a music directory, categorizes files by keywords in their names,
    and generates .m3u playlist files in the output directory.
    """
    if not os.path.isdir(music_dir):
        print(f"Error: Music directory '{music_dir}' not found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Define keyword to playlist name mappings
    keyword_playlists = {
        'bunker': 'Bunker_Beats',
        'scavenge': 'Scavenging_Soundtrack',
        'epic': 'Epic_Anthems',
        'chill': 'Chill_Out_Zone',
        'somber': 'Somber_Reflections',
        'hope': 'Glimmers_of_Hope',
        'radio': 'Static_Radio_Hits'
    }

    # Supported audio file extensions
    audio_extensions = ('.mp3', '.wav', '.ogg', '.flac')

    # Dictionary to hold playlist content
    playlists_content = {name: [] for name in keyword_playlists.values()}

    print(f"Scanning '{music_dir}' for audio files...")
    for root, _, files in os.walk(music_dir):
        for filename in files:
            if filename.lower().endswith(audio_extensions):
                full_path = os.path.join(root, filename)
                relative_path = os.path.relpath(full_path, music_dir)

                added_to_playlist = False
                for keyword, playlist_name in keyword_playlists.items():
                    if keyword in filename.lower():
                        playlists_content[playlist_name].append(relative_path)
                        added_to_playlist = True

                if added_to_playlist:
                    print(f"  Found: {filename}")

    print("\nGenerating playlists...")
    generated_count = 0
    for playlist_name, files_in_playlist in playlists_content.items():
        if files_in_playlist:
            playlist_filepath = os.path.join(output_dir, f"{playlist_name}.m3u")
            with open(playlist_filepath, 'w') as f:
                for file_path in files_in_playlist:
                    f.write(file_path + '\n')
            print(f"  Created '{playlist_name}.m3u' with {len(files_in_playlist)} tracks.")
            generated_count += 1

    if generated_count == 0:
        print("No playlists generated. Try adding keywords to your music filenames!")
    else:
        print(f"\nSuccessfully generated {generated_count} playlists in '{output_dir}'.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Apocalyptic Playlist Curator: Organizes music into themed playlists."
    )
    parser.add_argument(
        "music_dir",
        help="Path to the directory containing your music files."
    )
    parser.add_argument(
        "output_dir",
        help="Path to the directory where .m3u playlist files will be saved."
    )
    args = parser.parse_args()

    generate_playlists(args.music_dir, args.output_dir)
