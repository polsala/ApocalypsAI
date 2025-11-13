import unittest
import os
from unittest.mock import patch
from io import StringIO
from src.mood_ring import SystemMetrics, get_overlord_mood, main

class TestSystemMetrics(unittest.TestCase):
    def test_get_cpu_percent_mocked(self):
        # Mock rationale: We set an environment variable to control the mocked value
        # returned by SystemMetrics. This ensures deterministic testing without
        # relying on actual system calls.
        os.environ["MOCK_CPU_PERCENT"] = "75.5"
        metrics = SystemMetrics()
        self.assertEqual(metrics.get_cpu_percent(), 75.5)
        if "MOCK_CPU_PERCENT" in os.environ: del os.environ["MOCK_CPU_PERCENT"]

    def test_get_memory_percent_mocked(self):
        # Mock rationale: Same as above, for memory usage.
        os.environ["MOCK_MEMORY_PERCENT"] = "88.0"
        metrics = SystemMetrics()
        self.assertEqual(metrics.get_memory_percent(), 88.0)
        if "MOCK_MEMORY_PERCENT" in os.environ: del os.environ["MOCK_MEMORY_PERCENT"]

    def test_get_disk_percent_mocked(self):
        # Mock rationale: Same as above, for disk usage.
        os.environ["MOCK_DISK_PERCENT"] = "92.1"
        metrics = SystemMetrics()
        self.assertEqual(metrics.get_disk_percent(), 92.1)
        if "MOCK_DISK_PERCENT" in os.environ: del os.environ["MOCK_DISK_PERCENT"]

class TestOverlordMood(unittest.TestCase):
    def setUp(self):
        # Mock rationale: Reset environment variables before each test to ensure
        # test isolation and deterministic results.
        self.original_cpu = os.environ.get("MOCK_CPU_PERCENT")
        self.original_mem = os.environ.get("MOCK_MEMORY_PERCENT")
        self.original_disk = os.environ.get("MOCK_DISK_PERCENT")

    def tearDown(self):
        # Mock rationale: Restore original environment variables after each test.
        if self.original_cpu is not None:
            os.environ["MOCK_CPU_PERCENT"] = self.original_cpu
        else:
            if "MOCK_CPU_PERCENT" in os.environ: del os.environ["MOCK_CPU_PERCENT"]

        if self.original_mem is not None:
            os.environ["MOCK_MEMORY_PERCENT"] = self.original_mem
        else:
            if "MOCK_MEMORY_PERCENT" in os.environ: del os.environ["MOCK_MEMORY_PERCENT"]

        if self.original_disk is not None:
            os.environ["MOCK_DISK_PERCENT"] = self.original_disk
        else:
            if "MOCK_DISK_PERCENT" in os.environ: del os.environ["MOCK_DISK_PERCENT"]

    def set_mock_metrics(self, cpu: float, memory: float, disk: float):
        # Mock rationale: Helper to set the environment variables for specific test cases.
        os.environ["MOCK_CPU_PERCENT"] = str(cpu)
        os.environ["MOCK_MEMORY_PERCENT"] = str(memory)
        os.environ["MOCK_DISK_PERCENT"] = str(disk)

    def test_mood_enraged(self):
        # Mock rationale: Test case for the "Enraged" mood.
        self.set_mock_metrics(cpu=91, memory=50, disk=50)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Enraged")
        self.assertIn("Critical system resources are severely strained!", rationale)

        self.set_mock_metrics(cpu=50, memory=96, disk=50)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Enraged")

        self.set_mock_metrics(cpu=50, memory=50, disk=99)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Enraged")

    def test_mood_agitated(self):
        # Mock rationale: Test case for the "Agitated" mood.
        self.set_mock_metrics(cpu=75, memory=50, disk=50)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Agitated")
        self.assertIn("High resource usage detected.", rationale)

        self.set_mock_metrics(cpu=50, memory=86, disk=50)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Agitated")

        self.set_mock_metrics(cpu=50, memory=50, disk=91)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Agitated")

    def test_mood_pensive(self):
        # Mock rationale: Test case for the "Pensive" mood.
        self.set_mock_metrics(cpu=45, memory=50, disk=50)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Pensive")
        self.assertIn("Moderate resource activity.", rationale)

        self.set_mock_metrics(cpu=30, memory=75, disk=50)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Pensive")

        self.set_mock_metrics(cpu=30, memory=50, disk=85)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Pensive")

    def test_mood_bored(self):
        # Mock rationale: Test case for the "Bored" mood.
        self.set_mock_metrics(cpu=5, memory=20, disk=40)
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Bored")
        self.assertIn("System is idle. The Overlord seeks stimulation.", rationale)

    def test_mood_content(self):
        # Mock rationale: Test case for the "Content" mood (default/normal).
        self.set_mock_metrics(cpu=20, memory=40, disk=50) # Default values
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Content")
        self.assertIn("All systems nominal. The Overlord is pleased.", rationale)

        self.set_mock_metrics(cpu=35, memory=65, disk=75) # Just below pensive thresholds
        metrics = SystemMetrics()
        mood, rationale = get_overlord_mood(metrics)
        self.assertEqual(mood, "Content")

class TestMainFunction(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output(self, mock_stdout):
        # Mock rationale: We use patch to redirect stdout to a StringIO object
        # and set specific environment variables to control the mocked system metrics.
        # This allows us to test the console output of the main function deterministically.
        os.environ["MOCK_CPU_PERCENT"] = "25.0"
        os.environ["MOCK_MEMORY_PERCENT"] = "45.0"
        os.environ["MOCK_DISK_PERCENT"] = "55.0"

        main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("The AI Overlord is feeling: Content.", output)
        self.assertIn("All systems nominal. The Overlord is pleased.", output)

        if "MOCK_CPU_PERCENT" in os.environ: del os.environ["MOCK_CPU_PERCENT"]
        if "MOCK_MEMORY_PERCENT" in os.environ: del os.environ["MOCK_MEMORY_PERCENT"]
        if "MOCK_DISK_PERCENT" in os.environ: del os.environ["MOCK_DISK_PERCENT"]

    @patch('sys.stdout', new_callable=StringIO)
    def test_main_output_agitated(self, mock_stdout):
        # Mock rationale: Another test for main output, simulating an "Agitated" state.
        os.environ["MOCK_CPU_PERCENT"] = "75.0"
        os.environ["MOCK_MEMORY_PERCENT"] = "60.0"
        os.environ["MOCK_DISK_PERCENT"] = "70.0"

        main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("The AI Overlord is feeling: Agitated.", output)
        self.assertIn("High resource usage detected. The Overlord is displeased.", output)

        if "MOCK_CPU_PERCENT" in os.environ: del os.environ["MOCK_CPU_PERCENT"]
        if "MOCK_MEMORY_PERCENT" in os.environ: del os.environ["MOCK_MEMORY_PERCENT"]
        if "MOCK_DISK_PERCENT" in os.environ: del os.environ["MOCK_DISK_PERCENT"]


if __name__ == '__main__':
    unittest.main()
