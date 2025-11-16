import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
from collections import defaultdict

# Add the src directory to the Python path for importing echoes_engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from echoes_engine import EchoesEngine

class TestEchoesEngine(unittest.TestCase):

    def setUp(self):
        self.engine = EchoesEngine()
        self.mock_music_dir = '/mock/music'
        self.mock_output_dir = '/mock/output'

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_scan_music_directory_empty(self, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to confirm the music directory exists.
        # os.walk is mocked to simulate an empty directory structure.
        mock_isdir.return_value = True
        mock_walk.return_value = [] # No files or subdirectories
        
        tracks = self.engine.scan_music_directory(self.mock_music_dir)
        self.assertEqual(tracks, defaultdict(list))
        mock_isdir.assert_called_once_with(self.mock_music_dir)
        mock_walk.assert_called_once_with(self.mock_music_dir)

    @patch('os.path.isdir')
    def test_scan_music_directory_not_found(self, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to simulate a non-existent music directory,
        # ensuring the FileNotFoundError is raised.
        mock_isdir.return_value = False
        with self.assertRaises(FileNotFoundError):
            self.engine.scan_music_directory(self.mock_music_dir)
        mock_isdir.assert_called_once_with(self.mock_music_dir)

    @patch('os.path.isdir')
    @patch('os.walk')
    def test_scan_music_directory_with_files(self, mock_walk, mock_isdir):
        # Mock rationale: os.path.isdir is mocked to confirm the music directory exists.
        # os.walk is mocked to simulate a directory structure with various audio files
        # and non-audio files, allowing for deterministic testing of file filtering and categorization.
        mock_isdir.return_value = True
        mock_walk.return_value = [
            (self.mock_music_dir, ['ambient_tunes', 'action_tracks'], ['unknown.txt', 'old_radio_broadcast.mp3']),
            (os.path.join(self.mock_music_dir, 'ambient_tunes'), [], ['calm_waters.mp3', 'deep_sleep.ogg']),
            (os.path.join(self.mock_music_dir, 'action_tracks'), [], ['epic_clash.wav', 'run_for_your_life.mp3', 'focus_track.mp3'])
        ]

        expected_tracks = defaultdict(list, {
            'Broadcasts & Signals': [os.path.join(self.mock_music_dir, 'old_radio_broadcast.mp3')],
            'Chill & Relax': [
                os.path.join(self.mock_music_dir, 'ambient_tunes', 'calm_waters.mp3'),
                os.path.join(self.mock_music_dir, 'ambient_tunes', 'deep_sleep.ogg')
            ],
            'Action & Adventure': [
                os.path.join(self.mock_music_dir, 'action_tracks', 'epic_clash.wav'),
                os.path.join(self.mock_music_dir, 'action_tracks', 'run_for_your_life.mp3')
            ],
            'Focus & Productivity': [
                os.path.join(self.mock_music_dir, 'action_tracks', 'focus_track.mp3')
            ]
        })

        tracks = self.engine.scan_music_directory(self.mock_music_dir)
        
        # Sort lists for deterministic comparison
        for category in tracks:
            tracks[category].sort()
        for category in expected_tracks:
            expected_tracks[category].sort()

        self.assertEqual(tracks, expected_tracks)

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_playlists(self, mock_file_open, mock_makedirs):
        # Mock rationale: os.makedirs is mocked to prevent actual directory creation.
        # builtins.open is mocked to capture the content written to playlist files,
        # allowing verification of the playlist format and content without touching the filesystem.
        tracks_by_category = defaultdict(list, {
            'Chill & Relax': [
                '/mock/music/ambient_tunes/calm_waters.mp3',
                '/mock/music/ambient_tunes/deep_sleep.ogg'
            ],
            'Action & Adventure': [
                '/mock/music/action_tracks/epic_clash.wav',
                '/mock/music/action_tracks/run_for_your_life.mp3'
            ]
        })

        generated_files = self.engine.generate_playlists(tracks_by_category, self.mock_output_dir)

        mock_makedirs.assert_called_once_with(self.mock_output_dir, exist_ok=True)
        self.assertEqual(len(generated_files), 2)
        self.assertIn(os.path.join(self.mock_output_dir, 'Chill_and_Relax.m3u'), generated_files)
        self.assertIn(os.path.join(self.mock_output_dir, 'Action_and_Adventure.m3u'), generated_files)

        # Verify content of Chill & Relax playlist
        mock_file_open.assert_any_call(os.path.join(self.mock_output_dir, 'Chill_and_Relax.m3u'), 'w', encoding='utf-8')
        handle = mock_file_open()
        handle.write.assert_any_call('#EXTM3U\n')
        handle.write.assert_any_call('/mock/music/ambient_tunes/calm_waters.mp3\n')
        handle.write.assert_any_call('/mock/music/ambient_tunes/deep_sleep.ogg\n')

        # Verify content of Action & Adventure playlist
        mock_file_open.assert_any_call(os.path.join(self.mock_output_dir, 'Action_and_Adventure.m3u'), 'w', encoding='utf-8')
        handle = mock_file_open()
        handle.write.assert_any_call('#EXTM3U\n')
        handle.write.assert_any_call('/mock/music/action_tracks/epic_clash.wav\n')
        handle.write.assert_any_call('/mock/music/action_tracks/run_for_your_life.mp3\n')

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_playlists_empty_category(self, mock_file_open, mock_makedirs):
        # Mock rationale: os.makedirs is mocked to prevent actual directory creation.
        # builtins.open is mocked to ensure no files are written when a category is empty.
        tracks_by_category = defaultdict(list, {
            'Empty Category': []
        })
        generated_files = self.engine.generate_playlists(tracks_by_category, self.mock_output_dir)
        self.assertEqual(len(generated_files), 0)
        mock_file_open.assert_not_called()

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(music_dir='/mock/music', output_dir='/mock/output'))
    @patch('echoes_engine.EchoesEngine.scan_music_directory', return_value=defaultdict(list, {'Chill & Relax': ['/mock/music/track1.mp3']}))
    @patch('echoes_engine.EchoesEngine.generate_playlists', return_value=['/mock/output/Chill_and_Relax.m3u'])
    @patch('builtins.print')
    def test_main_success(self, mock_print, mock_generate, mock_scan, mock_parse_args, mock_open, mock_makedirs):
        # Mock rationale: All external interactions (arg parsing, file system operations, printing) are mocked
        # to isolate the main function's logic and verify its flow and output messages.
        from echoes_engine import main
        main()
        mock_scan.assert_called_once_with('/mock/music')
        mock_generate.assert_called_once_with(mock_scan.return_value, '/mock/output')
        mock_print.assert_any_call("Successfully generated 1 playlists in '/mock/output/':")
        mock_print.assert_any_call("  - Chill_and_Relax.m3u")

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(music_dir='/mock/music', output_dir='/mock/output'))
    @patch('echoes_engine.EchoesEngine.scan_music_directory', side_effect=FileNotFoundError('Test Error'))
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_file_not_found_error(self, mock_exit, mock_print, mock_scan, mock_parse_args, mock_open, mock_makedirs):
        # Mock rationale: Similar to test_main_success, but specifically tests error handling
        # when scan_music_directory raises a FileNotFoundError.
        from echoes_engine import main
        main()
        mock_print.assert_any_call("Error: Test Error")
        mock_exit.assert_called_once_with(1)

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(music_dir='/mock/music', output_dir='/mock/output'))
    @patch('echoes_engine.EchoesEngine.scan_music_directory', return_value=defaultdict(list))
    @patch('builtins.print')
    def test_main_no_audio_files_found(self, mock_print, mock_scan, mock_parse_args, mock_open, mock_makedirs):
        # Mock rationale: Tests the scenario where no audio files are found, ensuring the correct message is printed.
        from echoes_engine import main
        main()
        mock_print.assert_any_call("No audio files found in '/mock/music'. No playlists generated.")
        mock_scan.assert_called_once_with('/mock/music')


if __name__ == '__main__':
    unittest.main()
