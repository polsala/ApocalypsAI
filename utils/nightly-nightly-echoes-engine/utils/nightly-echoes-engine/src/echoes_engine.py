import os
import argparse
from collections import defaultdict

class EchoesEngine:
    def __init__(self):
        self.categories = {
            'chill': 'Chill & Relax',
            'relax': 'Chill & Relax',
            'ambient': 'Chill & Relax',
            'sleep': 'Chill & Relax',
            'action': 'Action & Adventure',
            'fight': 'Action & Adventure',
            'epic': 'Action & Adventure',
            'run': 'Action & Adventure',
            'focus': 'Focus & Productivity',
            'work': 'Focus & Productivity',
            'study': 'Focus & Productivity',
            'radio': 'Broadcasts & Signals',
            'broadcast': 'Broadcasts & Signals',
            'news': 'Broadcasts & Signals',
        }
        self.audio_extensions = ('.mp3', '.wav', '.ogg', '.flac', '.aac')

    def _get_category_from_text(self, text):
        text_lower = text.lower()
        for keyword, category_name in self.categories.items():
            if keyword in text_lower:
                return category_name
        return 'Miscellaneous Echoes'

    def scan_music_directory(self, music_dir):
        if not os.path.isdir(music_dir):
            raise FileNotFoundError(f"Music directory not found: {music_dir}")

        tracks_by_category = defaultdict(list)
        for root, _, files in os.walk(music_dir):
            for file in files:
                if file.lower().endswith(self.audio_extensions):
                    filepath = os.path.join(root, file)
                    
                    # Infer category from filename and parent directory names
                    category = self._get_category_from_text(file)
                    if category == 'Miscellaneous Echoes': # Try parent dirs if filename didn't yield a category
                        parent_dir_name = os.path.basename(root)
                        if parent_dir_name:
                            category = self._get_category_from_text(parent_dir_name)
                    
                    tracks_by_category[category].append(filepath)
        return tracks_by_category

    def generate_playlists(self, tracks_by_category, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        generated_files = []

        for category, tracks in tracks_by_category.items():
            if not tracks:
                continue
            
            # Sanitize category name for filename
            playlist_filename = f"{category.replace(' ', '_').replace('&', 'and')}.m3u"
            playlist_path = os.path.join(output_dir, playlist_filename)
            
            with open(playlist_path, 'w', encoding='utf-8') as f:
                f.write('#EXTM3U\n') # M3U header
                for track_path in sorted(tracks):
                    f.write(f"{track_path}\n")
            generated_files.append(playlist_path)
        return generated_files

def main():
    parser = argparse.ArgumentParser(
        description="Nightly Echoes Engine: Generate curated playlists from your music library."
    )
    parser.add_argument(
        "--music-dir", 
        required=True, 
        help="The root directory containing your audio files."
    )
    parser.add_argument(
        "--output-dir", 
        default=os.path.join(os.path.dirname(__file__), '..', 'playlists'), 
        help="The directory where generated .m3u playlists will be saved."
    )

    args = parser.parse_args()

    engine = EchoesEngine()
    try:
        tracks_by_category = engine.scan_music_directory(args.music_dir)
        if not tracks_by_category:
            print(f"No audio files found in '{args.music_dir}'. No playlists generated.")
            return
        
        generated_playlists = engine.generate_playlists(tracks_by_category, args.output_dir)
        print(f"Successfully generated {len(generated_playlists)} playlists in '{args.output_dir}':")
        for playlist in generated_playlists:
            print(f"  - {os.path.basename(playlist)}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == '__main__':
    main()
