use std::io::{self, Read};

/// Represents a 2D map as a vector of character vectors.
type Map = Vec<Vec<char>>;

/// Finds the starting position 'S' on the map.
/// Returns `Some((row, col))` if found, `None` otherwise.
fn find_start(map: &Map) -> Option<(usize, usize)> {
    for (r, row) in map.iter().enumerate() {
        for (c, &cell) in row.iter().enumerate() {
            if cell == 'S' {
                return Some((r, c));
            }
        }
    }
    None
}

/// Calculates the echo distance in a given direction.
/// `dr` and `dc` are the row and column increments for the direction.
fn calculate_echo_distance(
    map: &Map,
    start_row: usize,
    start_col: usize,
    dr: isize,
    dc: isize,
) -> usize {
    let mut distance = 0;
    let mut current_row = start_row as isize;
    let mut current_col = start_col as isize;

    loop {
        current_row += dr;
        current_col += dc;
        distance += 1;

        // Check map boundaries
        if current_row < 0
            || current_row >= map.len() as isize
            || current_col < 0
            || current_col >= map[0].len() as isize
        {
            return distance; // Hit boundary
        }

        let r = current_row as usize;
        let c = current_col as usize;

        // Check for obstacle
        if map[r][c] == '#' {
            return distance; // Hit obstacle
        }
    }
}

/// Parses a string input into a 2D map.
fn parse_map_input(input: &str) -> Result<Map, String> {
    let lines: Vec<&str> = input.lines().filter(|l| !l.trim().is_empty()).collect();
    if lines.is_empty() {
        return Err("Input map is empty.".to_string());
    }

    let mut map: Map = Vec::new();
    let mut expected_width: Option<usize> = None;

    for line in lines {
        let trimmed_line = line.trim();
        if trimmed_line.is_empty() {
            continue;
        }

        let current_width = trimmed_line.chars().count();
        if let Some(width) = expected_width {
            if width != current_width {
                return Err(format!("Inconsistent row length. Expected {}, got {}.\nLine: '{}'", width, current_width, trimmed_line));
            }
        } else {
            expected_width = Some(current_width);
        }
        map.push(trimmed_line.chars().collect());
    }

    if map.is_empty() {
        return Err("No valid map rows found.".to_string());
    }

    Ok(map)
}

fn main() -> Result<(), String> {
    let mut buffer = String::new();
    io::stdin()
        .read_to_string(&mut buffer)
        .map_err(|e| format!("Failed to read from stdin: {}", e))?;

    let map = parse_map_input(&buffer)?;

    if map.is_empty() || map[0].is_empty() {
        return Err("Map is empty or malformed.".to_string());
    }

    let (start_row, start_col) = find_start(&map).ok_or("Starting position 'S' not found on the map.")?;

    println!("Echo Distances:");
    println!("North: {}", calculate_echo_distance(&map, start_row, start_col, -1, 0));
    println!("South: {}", calculate_echo_distance(&map, start_row, start_col, 1, 0));
    println!("East: {}", calculate_echo_distance(&map, start_row, start_col, 0, 1));
    println!("West: {}", calculate_echo_distance(&map, start_row, start_col, 0, -1));

    Ok(())
}
