import heapq
import argparse
import sys

class Node:
    """
    Represents a node in the grid for pathfinding.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = float('inf')  # Cost from start to this node
        self.h = 0             # Heuristic cost from this node to end
        self.f = float('inf')  # Total cost (g + h)
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

class Grid:
    """
    Represents the wasteland grid.
    """
    def __init__(self, width, height, hazards=None):
        self.width = width
        self.height = height
        self.hazards = set(hazards) if hazards else set()

    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and (x, y) not in self.hazards

    def get_neighbors(self, node):
        neighbors = []
        # 4-directional movement (up, down, left, right)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = node.x + dx, node.y + dy
            if self.is_valid(nx, ny):
                neighbors.append(Node(nx, ny))
        return neighbors

def heuristic(node, end_node):
    """
    Manhattan distance heuristic.
    """
    return abs(node.x - end_node.x) + abs(node.y - end_node.y)

def a_star_search(grid, start_coords, end_coords):
    """
    Finds the shortest path using the A* algorithm.
    """
    start_node = Node(start_coords[0], start_coords[1])
    end_node = Node(end_coords[0], end_coords[1])

    if not grid.is_valid(start_node.x, start_node.y) or \
       not grid.is_valid(end_node.x, end_node.y):
        return None # Start or end is in a hazard

    open_set = []
    # Use a dictionary for faster lookup of nodes already in open_set or closed_set
    # and to update their properties if a better path is found.
    # This maps (x,y) -> Node object
    all_nodes = {}

    start_node.g = 0
    start_node.h = heuristic(start_node, end_node)
    start_node.f = start_node.g + start_node.h
    heapq.heappush(open_set, start_node)
    all_nodes[(start_node.x, start_node.y)] = start_node

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node == end_node:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1] # Reverse to get path from start to end

        for neighbor_coords in grid.get_neighbors(current_node):
            # Get the actual neighbor node from all_nodes or create if new
            if (neighbor_coords.x, neighbor_coords.y) not in all_nodes:
                neighbor = neighbor_coords
                all_nodes[(neighbor.x, neighbor.y)] = neighbor
            else:
                neighbor = all_nodes[(neighbor_coords.x, neighbor_coords.y)]

            tentative_g_score = current_node.g + 1 # Cost to move to neighbor is 1

            if tentative_g_score < neighbor.g:
                neighbor.parent = current_node
                neighbor.g = tentative_g_score
                neighbor.h = heuristic(neighbor, end_node)
                neighbor.f = neighbor.g + neighbor.h
                if neighbor not in open_set: # Check if neighbor is already in open_set (heapq doesn't have direct 'in' check for objects)
                    # A more robust way for heapq is to track items in a set or update existing ones.
                    # For simplicity, we'll push duplicates and handle them when popped (if current.g is worse than stored, ignore).
                    # A better approach would be to use a dict for open_set and update values, then re-heapify or use a more complex structure.
                    # For this problem, pushing duplicates is acceptable as long as we check current_node.g.
                    heapq.heappush(open_set, neighbor)
                # If it's already in open_set, and we found a better path, it will be processed later with the better g_score.

    return None # No path found

def parse_coords(coord_str):
    try:
        x, y = map(int, coord_str.split(','))
        return x, y
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid coordinate format: {coord_str}. Expected x,y")

def print_grid(grid, path, start, end):
    sys.stdout.write(f"Wasteland Grid ({grid.width}x{grid.height}):\n")
    grid_map = [['.' for _ in range(grid.width)] for _ in range(grid.height)]

    for hx, hy in grid.hazards:
        if 0 <= hx < grid.width and 0 <= hy < grid.height:
            grid_map[hy][hx] = 'X'

    for px, py in path:
        if (px, py) == start:
            grid_map[py][px] = 'S'
        elif (px, py) == end:
            grid_map[py][px] = 'E'
        else:
            grid_map[py][px] = '#'

    # Mark start and end if they are not part of the path (e.g., path is just start-end)
    if grid_map[start[1]][start[0]] == '.':
        grid_map[start[1]][start[0]] = 'S'
    if grid_map[end[1]][end[0]] == '.':
        grid_map[end[1]][end[0]] = 'E'

    for row in grid_map:
        sys.stdout.write(' '.join(row) + '\n')

def main():
    parser = argparse.ArgumentParser(
        description="Find the shortest path through a wasteland grid, avoiding hazards."
    )
    parser.add_argument("--grid-width", type=int, required=True,
                        help="The width of the grid (number of columns).")
    parser.add_argument("--grid-height", type=int, required=True,
                        help="The height of the grid (number of rows).")
    parser.add_argument("--start", type=parse_coords, required=True,
                        help="The starting coordinates (x,y).")
    parser.add_argument("--end", type=parse_coords, required=True,
                        help="The ending coordinates (x,y).")
    parser.add_argument("--hazard", type=parse_coords, action="append", default=[],
                        help="Coordinates of a hazardous zone (x,y). Can be repeated.")

    args = parser.parse_args()

    # Input validation
    if not (0 <= args.start[0] < args.grid_width and 0 <= args.start[1] < args.grid_height):
        sys.stderr.write(f"Error: Start coordinates {args.start} are out of grid bounds.\n")
        sys.exit(1)
    if not (0 <= args.end[0] < args.grid_width and 0 <= args.end[1] < args.grid_height):
        sys.stderr.write(f"Error: End coordinates {args.end} are out of grid bounds.\n")
        sys.exit(1)

    grid = Grid(args.grid_width, args.grid_height, args.hazard)

    sys.stdout.write(f"Wasteland Grid ({grid.width}x{grid.height}):\n")
    initial_grid_map = [['.' for _ in range(grid.width)] for _ in range(grid.height)]
    for hx, hy in grid.hazards:
        if 0 <= hx < grid.width and 0 <= hy < grid.height:
            initial_grid_map[hy][hx] = 'X'
    initial_grid_map[args.start[1]][args.start[0]] = 'S'
    initial_grid_map[args.end[1]][args.end[0]] = 'E'
    for row in initial_grid_map:
        sys.stdout.write(' '.join(row) + '\n')
    sys.stdout.write('\n')


    path = a_star_search(grid, args.start, args.end)

    if path:
        sys.stdout.write("Path found!\n")
        print_grid(grid, path, args.start, args.end)
        sys.stdout.write(f"\nPath length: {len(path) - 1} steps\n") # -1 because path includes start
    else:
        sys.stdout.write("No path found through the wasteland. You're doomed!\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
