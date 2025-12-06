import unittest
from unittest.mock import patch
from io import StringIO
from src.planner import find_path, visualize_path, main

class TestWastelandScavengerPlanner(unittest.TestCase):

    def test_find_path_simple_straight(self):
        # Mock rationale: Simulating a simple map grid for direct pathfinding.
        map_grid = [
            "S.R"
        ]
        path, length = find_path(map_grid)
        self.assertIsNotNone(path)
        self.assertEqual(length, 1)
        self.assertEqual(path, [(0, 0), (0, 2)]) # S to R

    def test_find_path_around_hazard(self):
        # Mock rationale: Simulating a map where the path needs to go around an obstacle.
        map_grid = [
            "S.X",
            "..R"
        ]
        path, length = find_path(map_grid)
        self.assertIsNotNone(path)
        self.assertEqual(length, 2)
        self.assertEqual(path, [(0, 0), (1, 0), (1, 2)]) # S -> (1,0) -> R

    def test_find_path_no_path(self):
        # Mock rationale: Simulating a map where the target is completely blocked.
        map_grid = [
            "SXR",
            "XXX",
            "E.X"
        ]
        path, length = find_path(map_grid)
        self.assertIsNone(path)
        self.assertIsNone(length)

    def test_find_path_multiple_targets_shortest_to_resource(self):
        # Mock rationale: Simulating a map with multiple targets (E and R) to ensure shortest path is chosen.
        map_grid = [
            "S.E",
            ".X.",
            "..R"
        ]
        path, length = find_path(map_grid)
        self.assertIsNotNone(path)
        # Path to E is (0,0)->(0,1)->(0,2) length 2
        # Path to R is (0,0)->(1,0)->(2,0)->(2,1)->(2,2) length 4
        # BFS finds E first as it's closer
        self.assertEqual(length, 2)
        self.assertEqual(path, [(0, 0), (0, 1), (0, 2)]) # S to E

    def test_find_path_no_start(self):
        # Mock rationale: Testing scenario where no start character is present.
        map_grid = [
            ".X.",
            "..R"
        ]
        path, length = find_path(map_grid)
        self.assertIsNone(path)
        self.assertIsNone(length)

    def test_find_path_no_target(self):
        # Mock rationale: Testing scenario where no target (E or R) is present.
        map_grid = [
            "S.X",
            ".X."
        ]
        path, length = find_path(map_grid)
        self.assertIsNone(path)
        self.assertIsNone(length)

    def test_find_path_start_is_target(self):
        # Mock rationale: Testing scenario where start is also a target.
        map_grid = [
            "S"
        ]
        path, length = find_path(map_grid, start_char='S', end_char='S')
        self.assertIsNotNone(path)
        self.assertEqual(length, 0)
        self.assertEqual(path, [(0,0)])

    def test_visualize_path_simple(self):
        # Mock rationale: Testing the visualization of a simple path.
        map_grid = ["S.R"]
        path = [(0, 0), (0, 1), (0, 2)]
        expected_output = "S>R"
        self.assertEqual(visualize_path(map_grid, path), expected_output)

    def test_visualize_path_with_turns(self):
        # Mock rationale: Testing visualization with turns and a longer path.
        map_grid = [
            "S..",
            ".X.",
            "..R"
        ]
        path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
        expected_output = "\n".join([
            "S>>",
            ".Xv",
            "..R"
        ])
        self.assertEqual(visualize_path(map_grid, path), expected_output)

    def test_visualize_path_no_path(self):
        # Mock rationale: Testing visualization when no path is found.
        map_grid = ["S.X", "X.R"]
        path = None
        expected_output = "\nNo path found."
        self.assertEqual(visualize_path(map_grid, path), expected_output)

    @patch('builtins.input', side_effect=['S.R', 'DONE'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_simple_path(self, mock_stdout, mock_input):
        # Mock rationale: Simulating user input and capturing stdout for the main function.
        # This tests the CLI interaction and overall flow.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Path found! Length: 1 steps.", output)
        self.assertIn("S>R", output)

    @patch('builtins.input', side_effect=['S.X', 'X.R', 'DONE'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_path(self, mock_stdout, mock_input):
        # Mock rationale: Simulating user input for a map with no path and capturing stdout.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No path could be found to any resource or exit point.", output)

    @patch('builtins.input', side_effect=['S.E', '.X.', '..R', 'DONE'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_multiple_targets(self, mock_stdout, mock_input):
        # Mock rationale: Simulating user input for a map with multiple targets and capturing stdout.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Path found! Length: 2 steps.", output)
        self.assertIn("S>E", output) # Should find path to E first

    @patch('builtins.input', side_effect=['S.R', 'X', 'S.E', 'DONE']) # S.R, then error, then S.E (which is also bad)
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_uneven_rows_error(self, mock_stdout, mock_input):
        # Mock rationale: Simulating user input with uneven rows to test input validation.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("All rows must have the same length. Please try again.", output)
        # It should print the error, then continue prompting. The valid 'S.R' map will be used.
        self.assertIn("Path found! Length: 1 steps.", output) # Path S.R should be found
        self.assertIn("S>R", output)

    @patch('builtins.input', side_effect=['', 'S.R', 'DONE'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_empty_row_error(self, mock_stdout, mock_input):
        # Mock rationale: Simulating user input with an empty row to test input validation.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Row cannot be empty. Please try again.", output)
        self.assertIn("Path found! Length: 1 steps.", output) # Should recover and process S.R

    @patch('builtins.input', side_effect=['DONE'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_no_map_provided(self, mock_stdout, mock_input):
        # Mock rationale: Simulating user immediately typing 'DONE' without providing a map.
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No map provided. Exiting.", output)


if __name__ == '__main__':
    unittest.main()
