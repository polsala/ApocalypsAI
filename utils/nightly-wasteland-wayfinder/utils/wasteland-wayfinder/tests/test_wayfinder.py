import unittest
from unittest.mock import patch, mock_open
import json
import os
from io import StringIO
from datetime import datetime

# Mock the current time for deterministic 'created_at' values
FIXED_DATETIME = '2077-10-23T08:00:00.000000'

# Mock rationale: We need to simulate file system operations (loading/saving tasks)
# without actually touching the disk. This ensures tests are fast, isolated, and deterministic.
# We also mock datetime.datetime.now() to ensure 'created_at' timestamps are consistent across test runs.

class TestWastelandWayfinder(unittest.TestCase):

    @patch('os.path.exists', return_value=False)
    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('datetime.datetime')
    def test_add_task(self, mock_dt, mock_stdout, mock_file_open, mock_json_load, mock_json_dump, mock_exists):
        from src.wayfinder import add_task, DATA_FILE

        mock_dt.now.return_value = datetime.fromisoformat(FIXED_DATETIME)
        mock_json_load.return_value = [] # Initial state: no tasks

        add_task("Find water purifier", "high", ["Water", "Tools"])

        # Assert that json.dump was called with the correct data
        expected_task = {
            'id': 1,
            'description': "Find water purifier",
            'urgency': 3, # high
            'resources': ["Tools", "Water"], # Sorted alphabetically
            'completed': False,
            'created_at': FIXED_DATETIME
        }
        mock_json_dump.assert_called_once_with([expected_task], mock_file_open(), indent=4)
        self.assertIn("Task 'Find water purifier' added with ID 1.", mock_stdout.getvalue())

        # Test adding another task
        mock_json_load.return_value = [expected_task] # Simulate previous task existing
        mock_json_dump.reset_mock()
        mock_stdout.seek(0); mock_stdout.truncate(0)

        add_task("Secure perimeter", "critical", ["ScrapMetal"])
        expected_task_2 = {
            'id': 2,
            'description': "Secure perimeter",
            'urgency': 4, # critical
            'resources': ["ScrapMetal"],
            'completed': False,
            'created_at': FIXED_DATETIME
        }
        mock_json_dump.assert_called_once_with([expected_task, expected_task_2], mock_file_open(), indent=4)
        self.assertIn("Task 'Secure perimeter' added with ID 2.", mock_stdout.getvalue())

    @patch('os.path.exists', return_value=True)
    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_tasks(self, mock_stdout, mock_file_open, mock_json_load, mock_json_dump, mock_exists):
        from src.wayfinder import list_tasks

        mock_tasks = [
            {
                'id': 1,
                'description': "Gather berries",
                'urgency': 2, # medium
                'resources': ["Food"],
                'completed': False,
                'created_at': FIXED_DATETIME
            },
            {
                'id': 2,
                'description': "Repair radio",
                'urgency': 3, # high
                'resources': ["Tools", "ScrapMetal"],
                'completed': True,
                'created_at': FIXED_DATETIME
            },
            {
                'id': 3,
                'description': "Scout new area",
                'urgency': 4, # critical
                'resources': ["Ammo", "Water"],
                'completed': False,
                'created_at': FIXED_DATETIME
            }
        ]
        mock_json_load.return_value = mock_tasks

        # Test listing active tasks
        list_tasks()
        output = mock_stdout.getvalue()
        
        expected_active_order = [
            "[ ] ID: 3 | Urgency: Critical | Resources: Ammo, Water          | Description: Scout new area",
            "[ ] ID: 1 | Urgency: Medium  | Resources: Food                 | Description: Gather berries"
        ]
        actual_active_lines = [line.strip() for line in output.split('\n') if line.strip().startswith('[ ]')]
        self.assertEqual(len(actual_active_lines), len(expected_active_order))
        for i in range(len(expected_active_order)):
            self.assertEqual(actual_active_lines[i], expected_active_order[i])

        mock_stdout.seek(0); mock_stdout.truncate(0)

        # Test listing all tasks (including completed)
        list_tasks(include_completed=True)
        output = mock_stdout.getvalue()
        expected_all_order = [
            "[ ] ID: 3 | Urgency: Critical | Resources: Ammo, Water          | Description: Scout new area",
            "[X] ID: 2 | Urgency: High      | Resources: ScrapMetal, Tools    | Description: Repair radio",
            "[ ] ID: 1 | Urgency: Medium  | Resources: Food                 | Description: Gather berries"
        ]
        actual_all_lines = [line.strip() for line in output.split('\n') if line.strip().startswith('[')]
        self.assertEqual(len(actual_all_lines), len(expected_all_order))
        for i in range(len(expected_all_order)):
            self.assertEqual(actual_all_lines[i], expected_all_order[i])

        # Test no tasks found
        mock_json_load.return_value = []
        mock_stdout.seek(0); mock_stdout.truncate(0)
        list_tasks()
        self.assertIn("No tasks found. Time to scavenge for new objectives!", mock_stdout.getvalue())

    @patch('os.path.exists', return_value=True)
    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_task(self, mock_stdout, mock_file_open, mock_json_load, mock_json_dump, mock_exists):
        from src.wayfinder import complete_task

        mock_tasks = [
            {
                'id': 1,
                'description': "Gather berries",
                'urgency': 2,
                'resources': ["Food"],
                'completed': False,
                'created_at': FIXED_DATETIME
            }
        ]
        mock_json_load.return_value = mock_tasks

        complete_task(1)

        expected_tasks_after_completion = [
            {
                'id': 1,
                'description': "Gather berries",
                'urgency': 2,
                'resources': ["Food"],
                'completed': True,
                'created_at': FIXED_DATETIME
            }
        ]
        mock_json_dump.assert_called_once_with(expected_tasks_after_completion, mock_file_open(), indent=4)
        self.assertIn("Task 'Gather berries' (ID: 1) marked as completed.", mock_stdout.getvalue())

        # Test completing a non-existent task
        mock_json_dump.reset_mock()
        mock_stdout.seek(0); mock_stdout.truncate(0)
        complete_task(99)
        mock_json_dump.assert_not_called() # No save should happen if task not found
        self.assertIn("Error: Task with ID 99 not found.", mock_stdout.getvalue())

    @patch('os.path.exists', return_value=False)
    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('datetime.datetime')
    def test_add_task_default_urgency_and_resources(self, mock_dt, mock_stdout, mock_file_open, mock_json_load, mock_json_dump, mock_exists):
        from src.wayfinder import add_task, DATA_FILE

        mock_dt.now.return_value = datetime.fromisoformat(FIXED_DATETIME)
        mock_json_load.return_value = []

        add_task("Explore ruins", "medium", [])

        expected_task = {
            'id': 1,
            'description': "Explore ruins",
            'urgency': 2, # medium
            'resources': [],
            'completed': False,
            'created_at': FIXED_DATETIME
        }
        mock_json_dump.assert_called_once_with([expected_task], mock_file_open(), indent=4)
        self.assertIn("Task 'Explore ruins' added with ID 1.", mock_stdout.getvalue())

    @patch('os.path.exists', return_value=True)
    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open', new_callable=mock_open)
    @patch('sys.stdout', new_callable=StringIO)
    def test_list_tasks_sorting(self, mock_stdout, mock_file_open, mock_json_load, mock_json_dump, mock_exists):
        from src.wayfinder import list_tasks

        mock_tasks = [
            {
                'id': 1,
                'description': "Gather berries",
                'urgency': 2, # medium
                'resources': ["Food"],
                'completed': False,
                'created_at': FIXED_DATETIME
            },
            {
                'id': 2,
                'description': "Repair radio",
                'urgency': 3, # high
                'resources': ["Tools", "ScrapMetal"],
                'completed': False,
                'created_at': FIXED_DATETIME
            },
            {
                'id': 3,
                'description': "Scout new area",
                'urgency': 4, # critical
                'resources': ["Ammo", "Water"],
                'completed': False,
                'created_at': FIXED_DATETIME
            },
            {
                'id': 4,
                'description': "Check traps",
                'urgency': 3, # high, same as Repair radio, but 'C' comes before 'R'
                'resources': ["Food"],
                'completed': False,
                'created_at': FIXED_DATETIME
            }
        ]
        mock_json_load.return_value = mock_tasks

        list_tasks()
        output = mock_stdout.getvalue()
        
        # Expected order: Scout new area (Crit), Check traps (High), Repair radio (High), Gather berries (Medium)
        expected_order = [
            "[ ] ID: 3 | Urgency: Critical | Resources: Ammo, Water          | Description: Scout new area",
            "[ ] ID: 4 | Urgency: High      | Resources: Food                 | Description: Check traps",
            "[ ] ID: 2 | Urgency: High      | Resources: ScrapMetal, Tools    | Description: Repair radio",
            "[ ] ID: 1 | Urgency: Medium  | Resources: Food                 | Description: Gather berries"
        ]
        
        # Filter out header/footer lines and empty lines, keeping only task lines
        actual_task_lines = [line.strip() for line in output.split('\n') if line.strip().startswith('[ ]') or line.strip().startswith('[X]')]
        
        self.assertEqual(len(actual_task_lines), len(expected_order))
        for i in range(len(expected_order)):
            self.assertEqual(actual_task_lines[i], expected_order[i])


if __name__ == '__main__':
    unittest.main()
