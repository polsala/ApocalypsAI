import unittest
import json
import os
import sys
from unittest.mock import patch, mock_open
from io import StringIO

# Mock rationale: We need to test the main function's file reading and printing behavior
# without actually creating files or printing to the console during tests.
# mock_open simulates file I/O, and patch('sys.stdout', new=StringIO()) captures print output.
# patch('sys.argv') allows us to simulate command-line arguments.

# Add the src directory to the path to allow importing prioritizer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from prioritizer import TaskScheduler, main, format_duration

class TestTaskScheduler(unittest.TestCase):

    def test_empty_tasks(self):
        scheduler = TaskScheduler([])
        result = scheduler.schedule()
        self.assertEqual(result['scheduled_tasks'], [])
        self.assertEqual(result['total_duration'], 0)
        self.assertEqual(result['critical_path_tasks'], [])

    def test_basic_tasks_no_dependencies(self):
        tasks_data = [
            {"name": "Task A", "duration": 30},
            {"name": "Task B", "duration": 60, "critical": True},
            {"name": "Task C", "duration": 45}
        ]
        scheduler = TaskScheduler(tasks_data)
        result = scheduler.schedule()
        
        # Order might vary for non-dependent tasks, but critical tasks should be prioritized if possible
        # Kahn's algorithm with sorting by (not critical, name)
        expected_names = ["Task B", "Task A", "Task C"] # B is critical, then A, C by name
        self.assertEqual([t['name'] for t in result['scheduled_tasks']], expected_names)
        self.assertEqual(result['total_duration'], 135)
        self.assertEqual(result['critical_path_tasks'], ["Task B"])

    def test_tasks_with_dependencies(self):
        tasks_data = [
            {"name": "Task A", "duration": 30},
            {"name": "Task B", "duration": 60, "dependencies": ["Task A"]},
            {"name": "Task C", "duration": 45, "dependencies": ["Task A"], "critical": True},
            {"name": "Task D", "duration": 15, "dependencies": ["Task B", "Task C"]}
        ]
        scheduler = TaskScheduler(tasks_data)
        result = scheduler.schedule()

        scheduled_names = [t['name'] for t in result['scheduled_tasks']]
        
        # Check topological order
        self.assertIn("Task A", scheduled_names[:1]) # A must be first
        self.assertTrue(scheduled_names.index("Task A") < scheduled_names.index("Task B"))
        self.assertTrue(scheduled_names.index("Task A") < scheduled_names.index("Task C"))
        self.assertTrue(scheduled_names.index("Task B") < scheduled_names.index("Task D"))
        self.assertTrue(scheduled_names.index("Task C") < scheduled_names.index("Task D"))

        self.assertEqual(result['total_duration'], 150) # 30+60+45+15
        self.assertEqual(result['critical_path_tasks'], ["Task C"])

    def test_circular_dependency_detection(self):
        tasks_data = [
            {"name": "Task A", "duration": 30, "dependencies": ["Task C"]},
            {"name": "Task B", "duration": 60, "dependencies": ["Task A"]},
            {"name": "Task C", "duration": 45, "dependencies": ["Task B"]}
        ]
        scheduler = TaskScheduler(tasks_data)
        result = scheduler.schedule()
        self.assertIn("error", result)
        self.assertIn("Circular dependency detected", result["error"])

    def test_missing_dependency(self):
        tasks_data = [
            {"name": "Task A", "duration": 30, "dependencies": ["NonExistentTask"]}
        ]
        with self.assertRaisesRegex(ValueError, "Dependency 'NonExistentTask' for task 'Task A' not found."):
            TaskScheduler(tasks_data)

    def test_critical_path_identification(self):
        tasks_data = [
            {"name": "Task 1", "duration": 10, "critical": True},
            {"name": "Task 2", "duration": 20},
            {"name": "Task 3", "duration": 30, "dependencies": ["Task 1"], "critical": True},
            {"name": "Task 4", "duration": 40, "dependencies": ["Task 2"]}
        ]
        scheduler = TaskScheduler(tasks_data)
        result = scheduler.schedule()
        self.assertIn("Task 1", result['critical_path_tasks'])
        self.assertIn("Task 3", result['critical_path_tasks'])
        self.assertNotIn("Task 2", result['critical_path_tasks'])
        self.assertNotIn("Task 4", result['critical_path_tasks'])
        
        # Check order of critical tasks in the list
        self.assertTrue(result['critical_path_tasks'].index("Task 1") < result['critical_path_tasks'].index("Task 3"))

    def test_format_duration(self):
        self.assertEqual(format_duration(0), "0 minutes")
        self.assertEqual(format_duration(1), "1 minute")
        self.assertEqual(format_duration(59), "59 minutes")
        self.assertEqual(format_duration(60), "1 hour")
        self.assertEqual(format_duration(61), "1 hour 1 minute")
        self.assertEqual(format_duration(120), "2 hours")
        self.assertEqual(format_duration(125), "2 hours 5 minutes")
        self.assertEqual(format_duration(180), "3 hours")

class TestMainFunction(unittest.TestCase):

    def setUp(self):
        # Capture stdout
        self.held_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        # Restore stdout
        sys.stdout = self.held_stdout

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"name": "Task A", "duration": 30},
        {"name": "Task B", "duration": 60, "critical": True}
    ]))
    @patch('sys.argv', ['prioritizer.py', 'tasks.json'])
    def test_main_success(self, mock_file_open):
        # Mock rationale: Simulate opening and reading a JSON file for tasks.
        # Mock sys.argv to provide the filename argument.
        with patch('sys.exit') as mock_exit:
            main()
            output = sys.stdout.getvalue()
            self.assertIn("Chronos-Chime Task Prioritizer Report", output)
            self.assertIn("Total estimated time: 1 hour 30 minutes", output)
            self.assertIn("1. Task B (1 hour) [CRITICAL PATH: Impending Doom!]", output)
            self.assertIn("2. Task A (30 minutes)", output)
            self.assertIn("Critical tasks identified: Task B", output)
            mock_exit.assert_not_called() # Should not exit on success

    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('sys.argv', ['prioritizer.py', 'tasks.json'])
    def test_main_invalid_json(self, mock_file_open):
        # Mock rationale: Simulate opening a file with malformed JSON.
        # Mock sys.argv to provide the filename argument.
        with patch('sys.exit') as mock_exit:
            main()
            output = sys.stdout.getvalue()
            self.assertIn("Error: Invalid JSON in 'tasks.json'", output)
            mock_exit.assert_called_once_with(1)

    @patch('builtins.open', side_effect=FileNotFoundError)
    @patch('sys.argv', ['prioritizer.py', 'non_existent_tasks.json'])
    def test_main_file_not_found(self, mock_file_open):
        # Mock rationale: Simulate a FileNotFoundError when trying to open the tasks file.
        # Mock sys.argv to provide the filename argument.
        with patch('sys.exit') as mock_exit:
            main()
            output = sys.stdout.getvalue()
            self.assertIn("Error: Task file not found at 'non_existent_tasks.json'", output)
            mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['prioritizer.py'])
    def test_main_no_arguments(self):
        # Mock rationale: Simulate running the script without any arguments.
        with patch('sys.exit') as mock_exit:
            main()
            output = sys.stdout.getvalue()
            self.assertIn("Usage: python prioritizer.py <path_to_tasks_json>", output)
            mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"name": "Task A", "duration": 30, "dependencies": ["Task C"]},
        {"name": "Task B", "duration": 60, "dependencies": ["Task A"]},
        {"name": "Task C", "duration": 45, "dependencies": ["Task B"]}
    ]))
    @patch('sys.argv', ['prioritizer.py', 'tasks.json'])
    def test_main_circular_dependency(self, mock_file_open):
        # Mock rationale: Simulate a tasks file with a circular dependency.
        # Mock sys.argv to provide the filename argument.
        with patch('sys.exit') as mock_exit:
            main()
            output = sys.stdout.getvalue()
            self.assertIn("Error: Circular dependency detected in tasks.", output)
            mock_exit.assert_called_once_with(1)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {"name": "Task A", "duration": 30, "dependencies": ["NonExistentTask"]}
    ]))
    @patch('sys.argv', ['prioritizer.py', 'tasks.json'])
    def test_main_missing_dependency_init_error(self, mock_file_open):
        # Mock rationale: Simulate a tasks file with a missing dependency, which causes an error during TaskScheduler initialization.
        # Mock sys.argv to provide the filename argument.
        with patch('sys.exit') as mock_exit:
            main()
            output = sys.stdout.getvalue()
            self.assertIn("An unexpected error occurred during scheduling: Dependency 'NonExistentTask' for task 'Task A' not found.", output)
            mock_exit.assert_called_once_with(1)
