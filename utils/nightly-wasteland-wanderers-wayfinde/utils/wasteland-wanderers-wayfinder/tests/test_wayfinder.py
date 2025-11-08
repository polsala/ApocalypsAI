import unittest
import sys
from unittest.mock import patch
from io import StringIO
from src.wayfinder import Node, Grid, a_star_search, heuristic, main, parse_coords

class TestNode(unittest.TestCase):
    def test_node_initialization(self):
        node = Node(1, 2)
        self.assertEqual(node.x, 1)
        self.assertEqual(node.y, 2)
        self.assertEqual(node.g, float('inf'))
        self.assertEqual(node.h, 0)
        self.assertEqual(node.f, float('inf'))
        self.assertIsNone(node.parent)

    def test_node_comparison(self):
        node1 = Node(0, 0)
        node1.f = 5
        node2 = Node(1, 1)
        node2.f = 10
        node3 = Node(2, 2)
        node3.f = 5

        self.assertTrue(node1 < node2)
        self.assertFalse(node2 < node1)
        self.assertFalse(node1 < node3) # f values are equal, order doesn't matter for <

    def test_node_equality(self):
        node1 = Node(0, 0)
        node2 = Node(0, 0)
        node3 = Node(1, 0)
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

    def test_node_hash(self):
        node1 = Node(0, 0)
        node2 = Node(0, 0)
        node3 = Node(1, 0)
        self.assertEqual(hash(node1), hash(node2))
        self.assertNotEqual(hash(node1), hash(node3))

class TestGrid(unittest.TestCase):
    def test_grid_initialization(self):
        grid = Grid(5, 5, hazards=[(1, 1), (2, 2)])
        self.assertEqual(grid.width, 5)
        self.assertEqual(grid.height, 5)
        self.assertIn((1, 1), grid.hazards)
        self.assertIn((2, 2), grid.hazards)
        self.assertNotIn((0, 0), grid.hazards)

    def test_is_valid(self):
        grid = Grid(3, 3, hazards=[(1, 1)])
        self.assertTrue(grid.is_valid(0, 0))
        self.assertFalse(grid.is_valid(1, 1)) # Hazard
        self.assertFalse(grid.is_valid(-1, 0)) # Out of bounds
        self.assertFalse(grid.is_valid(3, 0)) # Out of bounds

    def test_get_neighbors(self):
        grid = Grid(3, 3, hazards=[(1, 1)])
        node = Node(0, 0)
        neighbors = grid.get_neighbors(node)
        neighbor_coords = {(n.x, n.y) for n in neighbors}
        self.assertEqual(neighbor_coords, {(0, 1), (1, 0)})

        node = Node(1, 0)
        neighbors = grid.get_neighbors(node)
        neighbor_coords = {(n.x, n.y) for n in neighbors}
        # (1,1) is a hazard, so (1,1) should not be a neighbor
        self.assertEqual(neighbor_coords, {(0, 0), (2, 0)})

class TestHeuristic(unittest.TestCase):
    def test_manhattan_distance(self):
        node1 = Node(0, 0)
        node2 = Node(3, 4)
        self.assertEqual(heuristic(node1, node2), 7) # abs(0-3) + abs(0-4) = 3 + 4 = 7

        node3 = Node(1, 1)
        node4 = Node(1, 1)
        self.assertEqual(heuristic(node3, node4), 0)

class TestAStarSearch(unittest.TestCase):
    def test_simple_path(self):
        grid = Grid(3, 3)
        path = a_star_search(grid, (0, 0), (2, 2))
        expected_path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)] # One possible shortest path
        self.assertIsNotNone(path)
        self.assertEqual(len(path), 5) # 4 steps, 5 nodes
        # Verify path correctness (e.g., all steps are valid and connected)
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            self.assertTrue(abs(x1 - x2) + abs(y1 - y2) == 1) # Only cardinal moves

    def test_path_with_hazard(self):
        grid = Grid(3, 3, hazards=[(1, 0), (1, 1)]) # Block column 1
        path = a_star_search(grid, (0, 0), (2, 0))
        expected_path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0)]
        self.assertIsNotNone(path)
        self.assertEqual(path, expected_path)

    def test_no_path_blocked(self):
        grid = Grid(3, 3, hazards=[(0, 1), (1, 1), (2, 1)]) # Block middle row
        path = a_star_search(grid, (0, 0), (0, 2))
        self.assertIsNone(path)

    def test_start_is_hazard(self):
        grid = Grid(3, 3, hazards=[(0, 0)])
        path = a_star_search(grid, (0, 0), (2, 2))
        self.assertIsNone(path)

    def test_end_is_hazard(self):
        grid = Grid(3, 3, hazards=[(2, 2)])
        path = a_star_search(grid, (0, 0), (2, 2))
        self.assertIsNone(path)

    def test_large_grid_complex_path(self):
        grid = Grid(10, 10, hazards=[
            (1, 1), (1, 2), (1, 3), (1, 4),
            (2, 4), (3, 4), (4, 4), (5, 4),
            (5, 5), (5, 6), (5, 7), (5, 8)
        ])
        start = (0, 0)
        end = (9, 9)
        path = a_star_search(grid, start, end)
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)
        # Check that no hazard is in the path
        for px, py in path:
            self.assertNotIn((px, py), grid.hazards)
        # Check path validity (connected, within bounds)
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            self.assertTrue(abs(x1 - x2) + abs(y1 - y2) == 1) # Cardinal moves only
            self.assertTrue(grid.is_valid(x2, y2))

    def test_start_equals_end(self):
        grid = Grid(5, 5)
        path = a_star_search(grid, (2, 2), (2, 2))
        self.assertEqual(path, [(2, 2)])

class TestCLI(unittest.TestCase):
    # Mock rationale: We need to capture stdout and stderr to verify the CLI output
    # without actually printing to the console during tests.
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_simple_path_output(self, mock_parse_args, mock_stderr, mock_stdout):
        mock_parse_args.return_value = argparse.Namespace(
            grid_width=3, grid_height=3, start=(0, 0), end=(2, 2), hazard=[]
        )
        main()
        output = mock_stdout.getvalue()
        self.assertIn("Path found!", output)
        self.assertIn("S # .", output)
        self.assertIn(". # #", output)
        self.assertIn(". . E", output)
        self.assertIn("Path length: 4 steps", output)
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit') # Mock rationale: sys.exit is called on error, prevent test from exiting
    def test_main_no_path_output(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        mock_parse_args.return_value = argparse.Namespace(
            grid_width=3, grid_height=3, start=(0, 0), end=(0, 2), hazard=[(0, 1), (1, 1), (2, 1)]
        )
        main()
        output = mock_stdout.getvalue()
        self.assertIn("No path found through the wasteland. You're doomed!", output)
        mock_exit.assert_called_once_with(1)
        self.assertEqual(mock_stderr.getvalue(), "")

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_start_out_of_bounds(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        mock_parse_args.return_value = argparse.Namespace(
            grid_width=3, grid_height=3, start=(3, 0), end=(0, 0), hazard=[]
        )
        main()
        self.assertIn("Error: Start coordinates (3, 0) are out of grid bounds.", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stderr', new_callable=StringIO)
    @patch('argparse.ArgumentParser.parse_args')
    @patch('sys.exit')
    def test_main_end_out_of_bounds(self, mock_exit, mock_parse_args, mock_stderr, mock_stdout):
        mock_parse_args.return_value = argparse.Namespace(
            grid_width=3, grid_height=3, start=(0, 0), end=(-1, 0), hazard=[]
        )
        main()
        self.assertIn("Error: End coordinates (-1, 0) are out of grid bounds.", mock_stderr.getvalue())
        mock_exit.assert_called_once_with(1)

    def test_parse_coords_valid(self):
        self.assertEqual(parse_coords("1,2"), (1, 2))
        self.assertEqual(parse_coords("0,0"), (0, 0))

    def test_parse_coords_invalid(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_coords("1,2,3")
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_coords("1-2")
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_coords("a,b")

if __name__ == '__main__':
    unittest.main()
