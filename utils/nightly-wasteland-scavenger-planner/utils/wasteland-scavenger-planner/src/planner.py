import collections

def find_path(map_grid, start_char='S', end_char='E', resource_char='R', hazard_char='X'):
    """
    Finds a path from a start point to an end/resource point on a grid map, avoiding hazards.

    Args:
        map_grid (list of str): The map as a list of strings.
        start_char (str): Character representing the start point.
        end_char (str): Character representing the end/exit point.
        resource_char (str): Character representing a resource point.
        hazard_char (str): Character representing an impassable hazard.

    Returns:
        tuple: (path_coordinates, path_length) if a path is found, otherwise (None, None).
               path_coordinates is a list of (row, col) tuples.
    """
    rows = len(map_grid)
    cols = len(map_grid[0]) if rows > 0 else 0

    start = None
    targets = [] # Can be 'E' or 'R'

    for r in range(rows):
        for c in range(cols):
            if map_grid[r][c] == start_char:
                start = (r, c)
            elif map_grid[r][c] == end_char or map_grid[r][c] == resource_char:
                targets.append((r, c))

    if not start:
        return None, None # No start point found

    if not targets:
        return None, None # No target points found

    # BFS to find the shortest path
    queue = collections.deque([(start, [start])]) # (current_pos, path_so_far)
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) in targets:
            return path, len(path) - 1 # Return path and its length (number of steps)

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if map_grid[nr][nc] != hazard_char:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))

    return None, None # No path found to any target

def visualize_path(map_grid, path):
    """
    Visualizes the path on the map grid.
    """
    if not path:
        return "\nNo path found."

    rows = len(map_grid)
    cols = len(map_grid[0]) if rows > 0 else 0
    
    display_grid = [list(row) for row in map_grid]

    # Mark the path with arrows or a generic marker
    for i in range(len(path) - 1):
        r1, c1 = path[i]
        r2, c2 = path[i+1]

        # Only mark if the current cell is a traversable path ('.')
        # and not the start/end/resource itself
        if display_grid[r1][c1] == '.':
            if r2 > r1: display_grid[r1][c1] = 'v' # Down
            elif r2 < r1: display_grid[r1][c1] = '^' # Up
            elif c2 > c1: display_grid[r1][c1] = '>' # Right
            elif c2 < c1: display_grid[r1][c1] = '<' # Left
        
    # Ensure start and end/resource points are visible
    if path:
        start_r, start_c = path[0]
        display_grid[start_r][start_c] = map_grid[start_r][start_c] # Restore 'S'
        
        end_r, end_c = path[-1]
        display_grid[end_r][end_c] = map_grid[end_r][end_c] # Restore 'E' or 'R'

    return "\n".join(["".join(row) for row in display_grid])


def main():
    print("Welcome to the Wasteland Scavenger Planner!")
    print("Enter your map row by row. Type 'DONE' when finished.")
    print("Legend: S=Start, E=Exit, R=Resource, X=Hazard, .=Path")

    map_input = []
    while True:
        line = input(f"Row {len(map_input) + 1}: ").strip()
        if line.upper() == 'DONE':
            break
        if not line:
            print("Row cannot be empty. Please try again.")
            continue
        if map_input and len(line) != len(map_input[0]):
            print("All rows must have the same length. Please try again.")
            continue
        map_input.append(line)

    if not map_input:
        print("No map provided. Exiting.")
        return

    print("\nYour Map:")
    for row in map_input:
        print(row)

    path_coords, path_length = find_path(map_input)

    print("\n--- Planning Results ---")
    if path_coords:
        print(f"Path found! Length: {path_length} steps.")
        print("Path visualization:")
        print(visualize_path(map_input, path_coords))
    else:
        print("No path could be found to any resource or exit point.")

if __name__ == "__main__":
    main()
