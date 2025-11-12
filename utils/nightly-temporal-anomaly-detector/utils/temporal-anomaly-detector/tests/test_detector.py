import unittest
import os
import datetime
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Import the functions to be tested
from src.detector import find_temporal_anomalies, get_current_time_utc, get_file_mtime_utc

class TestTemporalAnomalyDetector(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        
        # Define a fixed current time for deterministic tests
        self.fixed_current_time = datetime.datetime(2023, 10, 26, 12, 0, 0, tzinfo=datetime.timezone.utc)
        
        # Define a future time
        self.future_time = datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        
        # Define an ancient time (more than 10 years before fixed_current_time)
        self.ancient_time = datetime.datetime(2010, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        
        # Define a normal time (within the 10-year window)
        self.normal_time = datetime.datetime(2022, 5, 15, 10, 30, 0, tzinfo=datetime.timezone.utc)

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    @patch('src.detector.datetime')
    @patch('src.detector.os.path')
    def test_find_temporal_anomalies_no_anomalies(self, mock_os_path, mock_datetime):
        # Mock rationale: Ensure deterministic current time for comparison.
        mock_datetime.datetime.now.return_value = self.fixed_current_time
        mock_datetime.timezone.utc = datetime.timezone.utc # Ensure timezone is correctly mocked
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts, tz: datetime.datetime.fromtimestamp(ts, tz)

        # Create a normal file
        normal_file_path = os.path.join(self.test_dir, "normal_file.txt")
        with open(normal_file_path, "w") as f:
            f.write("content")
        # Mock rationale: Control file modification time for deterministic test.
        mock_os_path.getmtime.return_value = self.normal_time.timestamp()
        
        # Mock rationale: Simulate directory walk for deterministic file discovery.
        mock_os_path.isdir.return_value = True
        with patch('src.detector.os.walk') as mock_walk:
            mock_walk.return_value = [
                (self.test_dir, [], ["normal_file.txt"])
            ]
            anomalies = find_temporal_anomalies(self.test_dir, max_age_years=10)
            self.assertEqual(len(anomalies), 0)

    @patch('src.detector.datetime')
    @patch('src.detector.os.path')
    def test_find_temporal_anomalies_future_file(self, mock_os_path, mock_datetime):
        # Mock rationale: Ensure deterministic current time for comparison.
        mock_datetime.datetime.now.return_value = self.fixed_current_time
        mock_datetime.timezone.utc = datetime.timezone.utc
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts, tz: datetime.datetime.fromtimestamp(ts, tz)

        # Create a future file
        future_file_path = os.path.join(self.test_dir, "future_file.txt")
        with open(future_file_path, "w") as f:
            f.write("content")
        # Mock rationale: Control file modification time to be in the future.
        mock_os_path.getmtime.return_value = self.future_time.timestamp()

        # Mock rationale: Simulate directory walk for deterministic file discovery.
        mock_os_path.isdir.return_value = True
        with patch('src.detector.os.walk') as mock_walk:
            mock_walk.return_value = [
                (self.test_dir, [], ["future_file.txt"])
            ]
            anomalies = find_temporal_anomalies(self.test_dir, max_age_years=10)
            self.assertEqual(len(anomalies), 1)
            self.assertEqual(anomalies[0]['type'], 'FUTURE')
            self.assertIn("future_file.txt", anomalies[0]['filepath'])
            self.assertEqual(anomalies[0]['mtime'], self.future_time)

    @patch('src.detector.datetime')
    @patch('src.detector.os.path')
    def test_find_temporal_anomalies_ancient_file(self, mock_os_path, mock_datetime):
        # Mock rationale: Ensure deterministic current time for comparison.
        mock_datetime.datetime.now.return_value = self.fixed_current_time
        mock_datetime.timezone.utc = datetime.timezone.utc
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts, tz: datetime.datetime.fromtimestamp(ts, tz)

        # Create an ancient file
        ancient_file_path = os.path.join(self.test_dir, "ancient_file.txt")
        with open(ancient_file_path, "w") as f:
            f.write("content")
        # Mock rationale: Control file modification time to be ancient.
        mock_os_path.getmtime.return_value = self.ancient_time.timestamp()

        # Mock rationale: Simulate directory walk for deterministic file discovery.
        mock_os_path.isdir.return_value = True
        with patch('src.detector.os.walk') as mock_walk:
            mock_walk.return_value = [
                (self.test_dir, [], ["ancient_file.txt"])
            ]
            anomalies = find_temporal_anomalies(self.test_dir, max_age_years=10)
            self.assertEqual(len(anomalies), 1)
            self.assertEqual(anomalies[0]['type'], 'ANCIENT')
            self.assertIn("ancient_file.txt", anomalies[0]['filepath'])
            self.assertEqual(anomalies[0]['mtime'], self.ancient_time)

    @patch('src.detector.datetime')
    @patch('src.detector.os.path')
    def test_find_temporal_anomalies_multiple_anomalies(self, mock_os_path, mock_datetime):
        # Mock rationale: Ensure deterministic current time for comparison.
        mock_datetime.datetime.now.return_value = self.fixed_current_time
        mock_datetime.timezone.utc = datetime.timezone.utc
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts, tz: datetime.datetime.fromtimestamp(ts, tz)

        # Create files
        future_file_path = os.path.join(self.test_dir, "future_file.txt")
        ancient_file_path = os.path.join(self.test_dir, "ancient_file.txt")
        normal_file_path = os.path.join(self.test_dir, "normal_file.txt")

        # Mock rationale: Control file modification times for deterministic test.
        # We need to mock getmtime to return different values for different files.
        # A simple way is to use a dictionary lookup or a side_effect function.
        mtime_map = {
            future_file_path: self.future_time.timestamp(),
            ancient_file_path: self.ancient_time.timestamp(),
            normal_file_path: self.normal_time.timestamp(),
        }
        mock_os_path.getmtime.side_effect = lambda p: mtime_map.get(p, self.normal_time.timestamp())

        # Mock rationale: Simulate directory walk for deterministic file discovery.
        mock_os_path.isdir.return_value = True
        with patch('src.detector.os.walk') as mock_walk:
            mock_walk.return_value = [
                (self.test_dir, [], ["future_file.txt", "ancient_file.txt", "normal_file.txt"])
            ]
            anomalies = find_temporal_anomalies(self.test_dir, max_age_years=10)
            self.assertEqual(len(anomalies), 2)
            anomaly_types = sorted([a['type'] for a in anomalies])
            self.assertEqual(anomaly_types, ['ANCIENT', 'FUTURE'])

    @patch('src.detector.datetime')
    @patch('src.detector.os.path')
    def test_find_temporal_anomalies_custom_max_age(self, mock_os_path, mock_datetime):
        # Mock rationale: Ensure deterministic current time for comparison.
        mock_datetime.datetime.now.return_value = self.fixed_current_time
        mock_datetime.timezone.utc = datetime.timezone.utc
        mock_datetime.datetime.fromtimestamp.side_effect = lambda ts, tz: datetime.datetime.fromtimestamp(ts, tz)

        # Define a time that is ancient for 5 years, but not for 10 years
        # fixed_current_time (2023) - 5 years = 2018
        # fixed_current_time (2023) - 10 years = 2013
        # So, a file from 2015 should be ancient with max_age_years=5, but not with max_age_years=10
        mid_ancient_time = datetime.datetime(2015, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        
        mid_ancient_file_path = os.path.join(self.test_dir, "mid_ancient_file.txt")
        with open(mid_ancient_file_path, "w") as f:
            f.write("content")
        mock_os_path.getmtime.return_value = mid_ancient_time.timestamp()

        mock_os_path.isdir.return_value = True
        with patch('src.detector.os.walk') as mock_walk:
            mock_walk.return_value = [
                (self.test_dir, [], ["mid_ancient_file.txt"])
            ]
            
            # Test with max_age_years = 5 (should be ancient)
            anomalies_5_years = find_temporal_anomalies(self.test_dir, max_age_years=5)
            self.assertEqual(len(anomalies_5_years), 1)
            self.assertEqual(anomalies_5_years[0]['type'], 'ANCIENT')

            # Test with max_age_years = 10 (should NOT be ancient)
            # Reset mock_os_path.getmtime for the second call if needed, or ensure it's consistent.
            # For this test, the mock_os_path.getmtime is set once, and os.walk is mocked.
            # The key is that find_temporal_anomalies is called twice with different max_age_years.
            # The mock_os_path.getmtime.return_value will persist, which is fine as it's the same file.
            anomalies_10_years = find_temporal_anomalies(self.test_dir, max_age_years=10)
            self.assertEqual(len(anomalies_10_years), 0) # 2015 is not older than 2013 (2023-10)

    @patch('src.detector.datetime')
    @patch('src.detector.os.path')
    def test_find_temporal_anomalies_non_existent_directory(self, mock_os_path, mock_datetime):
        # Mock rationale: Ensure deterministic current time for comparison.
        mock_datetime.datetime.now.return_value = self.fixed_current_time
        mock_datetime.timezone.utc = datetime.timezone.utc

        # Mock rationale: Simulate a non-existent directory.
        mock_os_path.isdir.return_value = False
        anomalies = find_temporal_anomalies("/non/existent/path", max_age_years=10)
        self.assertEqual(len(anomalies), 0) # Should return empty list and print error

if __name__ == '__main__':
    unittest.main()
