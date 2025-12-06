import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Add the src directory to the path to allow importing curator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import curator

class TestApocalypticPlaylistCurator(unittest.TestCase):

    @patch('os.makedirs')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_empty_music_directory(self, mock_file_open, mock_os_walk, mock_os_path_isdir, mock_os_makedirs):
        # Mock rationale: Simulate an empty music directory.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [('/mock/music', [], [])]

        curator.generate_playlists('/mock/music', '/mock/playlists')

        mock_os_makedirs.assert_called_once_with('/mock/playlists', exist_ok=True)
        mock_file_open.assert_not_called() # No playlists should be created

    @patch('os.makedirs')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_single_playlist_generation(self, mock_file_open, mock_os_walk, mock_os_path_isdir, mock_os_makedirs):
        # Mock rationale: Simulate a directory with files matching one keyword.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/music', [], ['song_bunker_1.mp3', 'another_bunker_track.wav', 'random_song.txt'])
        ]

        curator.generate_playlists('/mock/music', '/mock/playlists')

        mock_os_makedirs.assert_called_once_with('/mock/playlists', exist_ok=True)
        mock_file_open.assert_called_once_with(os.path.join('/mock/playlists', 'Bunker_Beats.m3u'), 'w')
        handle = mock_file_open()
        handle.write.assert_any_call('song_bunker_1.mp3\n')
        handle.write.assert_any_call('another_bunker_track.wav\n')
        self.assertEqual(handle.write.call_count, 2)

    @patch('os.makedirs')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_multiple_playlists_generation(self, mock_file_open, mock_os_walk, mock_os_path_isdir, mock_os_makedirs):
        # Mock rationale: Simulate a directory with files matching multiple keywords.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/music', [], [
                'epic_battle_theme.mp3',
                'chill_out_vibe.wav',
                'bunker_anthem.flac',
                'scavenge_walk.ogg',
                'non_audio_file.jpg'
            ])
        ]

        curator.generate_playlists('/mock/music', '/mock/playlists')

        mock_os_makedirs.assert_called_once_with('/mock/playlists', exist_ok=True)

        # Check that open was called for each expected playlist
        expected_calls = [
            unittest.mock.call(os.path.join('/mock/playlists', 'Epic_Anthems.m3u'), 'w'),
            unittest.mock.call(os.path.join('/mock/playlists', 'Chill_Out_Zone.m3u'), 'w'),
            unittest.mock.call(os.path.join('/mock/playlists', 'Bunker_Beats.m3u'), 'w'),
            unittest.mock.call(os.path.join('/mock/playlists', 'Scavenging_Soundtrack.m3u'), 'w')
        ]
        mock_file_open.assert_has_calls(expected_calls, any_order=True)

        # Verify content for a specific playlist (e.g., Epic_Anthems)
        # Note: mock_open captures all writes, so we need to check specific calls
        handle = mock_file_open()
        handle.write.assert_any_call('epic_battle_theme.mp3\n')
        handle.write.assert_any_call('chill_out_vibe.wav\n')
        handle.write.assert_any_call('bunker_anthem.flac\n')
        handle.write.assert_any_call('scavenge_walk.ogg\n')
        self.assertEqual(handle.write.call_count, 4) # Total unique audio files written

    @patch('os.makedirs')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_no_matching_keywords(self, mock_file_open, mock_os_walk, mock_os_path_isdir, mock_os_makedirs):
        # Mock rationale: Simulate audio files that do not match any predefined keywords.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/music', [], ['generic_song_1.mp3', 'another_tune.wav'])
        ]

        curator.generate_playlists('/mock/music', '/mock/playlists')

        mock_os_makedirs.assert_called_once_with('/mock/playlists', exist_ok=True)
        mock_file_open.assert_not_called() # No playlists should be created

    @patch('os.makedirs')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_non_existent_music_directory(self, mock_file_open, mock_os_walk, mock_os_path_isdir, mock_os_makedirs):
        # Mock rationale: Simulate a scenario where the music directory does not exist.
        mock_os_path_isdir.return_value = False

        curator.generate_playlists('/nonexistent/music', '/mock/playlists')

        mock_os_path_isdir.assert_called_once_with('/nonexistent/music')
        mock_os_makedirs.assert_not_called() # Output directory should not be created
        mock_file_open.assert_not_called()

    @patch('os.makedirs')
    @patch('os.path.isdir')
    @patch('os.walk')
    @patch('builtins.open', new_callable=mock_open)
    def test_nested_music_directory(self, mock_file_open, mock_os_walk, mock_os_path_isdir, mock_os_makedirs):
        # Mock rationale: Simulate a music directory with nested subdirectories.
        mock_os_path_isdir.return_value = True
        mock_os_walk.return_value = [
            ('/mock/music', ['subfolder'], ['bunker_track_main.mp3']),
            ('/mock/music/subfolder', [], ['scavenge_track_sub.wav'])
        ]

        curator.generate_playlists('/mock/music', '/mock/playlists')

        mock_os_makedirs.assert_called_once_with('/mock/playlists', exist_ok=True)
        mock_file_open.assert_any_call(os.path.join('/mock/playlists', 'Bunker_Beats.m3u'), 'w')
        mock_file_open.assert_any_call(os.path.join('/mock/playlists', 'Scavenging_Soundtrack.m3u'), 'w')

        handle = mock_file_open()
        handle.write.assert_any_call('bunker_track_main.mp3\n')
        handle.write.assert_any_call(os.path.join('subfolder', 'scavenge_track_sub.wav') + '\n')

if __name__ == '__main__':
    unittest.main()
