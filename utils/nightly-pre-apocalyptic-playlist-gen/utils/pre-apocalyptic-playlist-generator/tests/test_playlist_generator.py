import unittest
from unittest.mock import patch, mock_open
import json
import sys
import os

# Add the src directory to the path to allow importing playlist_generator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from playlist_generator import load_music_manifest, generate_playlist, main

class TestPlaylistGenerator(unittest.TestCase):

    def setUp(self):
        self.mock_manifest_content = {
            "calm": [
                {"title": "Weightless", "artist": "Marconi Union"},
                {"title": "Adagio for Strings", "artist": "Samuel Barber"},
                {"title": "Gymnopédie No. 1", "artist": "Erik Satie"}
            ],
            "energetic": [
                {"title": "Thunderstruck", "artist": "AC/DC"},
                {"title": "Sabotage", "artist": "Beastie Boys"}
            ],
            "empty_mood": [],
            "single_song_mood": [
                {"title": "One Song", "artist": "The Loner"}
            ]
        }
        self.mock_manifest_json = json.dumps(self.mock_manifest_content)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_load_music_manifest_success(self, mock_file, mock_exists):
        # Mock rationale: Simulates reading a valid JSON manifest file from disk.
        mock_file.return_value.read.return_value = self.mock_manifest_json
        manifest = load_music_manifest('dummy_path.json')
        self.assertEqual(manifest, self.mock_manifest_content)
        mock_file.assert_called_once_with('dummy_path.json', 'r', encoding='utf-8')

    @patch('os.path.exists', return_value=False)
    @patch('sys.exit')
    @patch('builtins.print')
    def test_load_music_manifest_file_not_found(self, mock_print, mock_exit, mock_exists):
        # Mock rationale: Simulates the scenario where the manifest file does not exist.
        load_music_manifest('non_existent.json')
        mock_print.assert_called_with("Error: Music manifest not found at 'non_existent.json'.", file=sys.stderr)
        mock_exit.assert_called_with(1)

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.exit')
    @patch('builtins.print')
    def test_load_music_manifest_invalid_json(self, mock_print, mock_exit, mock_file, mock_exists):
        # Mock rationale: Simulates reading a manifest file that contains malformed JSON.
        mock_file.return_value.read.return_value = "{invalid json"
        load_music_manifest('invalid.json')
        mock_print.assert_called_with("Error: Invalid JSON in 'invalid.json'.", file=sys.stderr)
        mock_exit.assert_called_with(1)

    @patch('random.sample')
    def test_generate_playlist_basic(self, mock_sample):
        # Mock rationale: Ensures deterministic selection of songs by controlling random.sample's output.
        mock_sample.return_value = [
            {"title": "Weightless", "artist": "Marconi Union"},
            {"title": "Adagio for Strings", "artist": "Samuel Barber"}
        ]
        playlist = generate_playlist('calm', 2, self.mock_manifest_content)
        self.assertEqual(len(playlist), 2)
        self.assertEqual(playlist[0]['title'], 'Weightless')
        mock_sample.assert_called_once_with(self.mock_manifest_content['calm'], 2)

    @patch('random.sample')
    @patch('builtins.print')
    def test_generate_playlist_count_exceeds_available(self, mock_print, mock_sample):
        # Mock rationale: Ensures deterministic selection when requested count is more than available songs.
        mock_sample.return_value = self.mock_manifest_content['energetic'] # Should return all available
        playlist = generate_playlist('energetic', 10, self.mock_manifest_content)
        self.assertEqual(len(playlist), 2)
        self.assertEqual(playlist, self.mock_manifest_content['energetic'])
        mock_sample.assert_called_once_with(self.mock_manifest_content['energetic'], len(self.mock_manifest_content['energetic']))
        mock_print.assert_called_with("Warning: Requested 10 songs, but only 2 available for mood 'energetic'. Returning all available songs.", file=sys.stderr)

    @patch('sys.exit')
    @patch('builtins.print')
    def test_generate_playlist_mood_not_found(self, mock_print, mock_exit):
        # Mock rationale: Simulates requesting a mood that does not exist in the manifest.
        generate_playlist('non_existent_mood', 5, self.mock_manifest_content)
        mock_print.assert_called_with("Error: Mood 'non_existent_mood' not found in the music manifest.", file=sys.stderr)
        mock_exit.assert_called_with(1)

    @patch('random.sample')
    @patch('builtins.print')
    def test_generate_playlist_empty_mood(self, mock_print, mock_sample):
        # Mock rationale: Simulates a mood category existing but containing no songs.
        playlist = generate_playlist('empty_mood', 5, self.mock_manifest_content)
        self.assertEqual(playlist, [])
        mock_print.assert_called_with("Warning: No songs found for mood 'empty_mood'. Returning an empty playlist.", file=sys.stderr)
        mock_sample.assert_not_called()

    @patch('random.sample')
    @patch('builtins.print')
    def test_generate_playlist_count_zero(self, mock_print, mock_sample):
        # Mock rationale: Tests behavior when a zero count is requested.
        playlist = generate_playlist('calm', 0, self.mock_manifest_content)
        self.assertEqual(playlist, [])
        mock_print.assert_called_with("Warning: Requested 0 songs. Returning an empty playlist.", file=sys.stderr)
        mock_sample.assert_not_called()

    @patch('random.sample')
    @patch('builtins.print')
    def test_generate_playlist_count_negative(self, mock_print, mock_sample):
        # Mock rationale: Tests behavior when a negative count is requested.
        playlist = generate_playlist('calm', -2, self.mock_manifest_content)
        self.assertEqual(playlist, [])
        mock_print.assert_called_with("Warning: Requested -2 songs. Returning an empty playlist.", file=sys.stderr)
        mock_sample.assert_not_called()

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('playlist_generator.load_music_manifest')
    @patch('playlist_generator.generate_playlist')
    @patch('argparse.ArgumentParser')
    def test_main_success(self, mock_argparse, mock_generate, mock_load, mock_stderr, mock_stdout):
        # Mock rationale: Mocks command-line arguments, manifest loading, and playlist generation
        # to test the main execution flow without actual file I/O or random selection.
        mock_args = unittest.mock.Mock()
        mock_args.mood = 'calm'
        mock_args.count = 2
        mock_args.manifest = 'dummy_path.json'
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_load.return_value = self.mock_manifest_content
        mock_generate.return_value = [
            {"title": "Weightless", "artist": "Marconi Union"},
            {"title": "Adagio for Strings", "artist": "Samuel Barber"}
        ]

        main()

        self.assertIn("--- Pre-Apocalyptic Playlist (calm) ---", mock_stdout.getvalue())
        self.assertIn("1. Weightless by Marconi Union", mock_stdout.getvalue())
        self.assertIn("2. Adagio for Strings by Samuel Barber", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=unittest.mock.StringIO)
    @patch('sys.stderr', new_callable=unittest.mock.StringIO)
    @patch('playlist_generator.load_music_manifest')
    @patch('playlist_generator.generate_playlist')
    @patch('argparse.ArgumentParser')
    def test_main_no_songs_generated(self, mock_argparse, mock_generate, mock_load, mock_stderr, mock_stdout):
        # Mock rationale: Mocks command-line arguments, manifest loading, and playlist generation
        # to test the main execution flow when no songs are returned (e.g., empty mood or count <= 0).
        mock_args = unittest.mock.Mock()
        mock_args.mood = 'empty_mood'
        mock_args.count = 5
        mock_args.manifest = 'dummy_path.json'
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_load.return_value = self.mock_manifest_content
        mock_generate.return_value = [] # Simulate no songs generated

        main()

        self.assertIn("No songs generated for mood 'empty_mood'.", mock_stdout.getvalue())
        self.assertEqual(mock_stderr.getvalue(), "")

if __name__ == '__main__':
    unittest.main()
