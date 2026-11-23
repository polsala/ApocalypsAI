#![allow(unused_imports)] // Allow unused imports for main functions if they are only used in tests

use super::{calculate_echo_distance, find_start, parse_map_input, Map};

// Mock rationale: These tests use in-memory string representations of maps and direct function calls.
// They do not interact with the file system or network, ensuring determinism and offline execution.

#[test]
fn test_parse_map_input_valid() {
    let input = "#####\n#S..#\n#.#.#\n#...#\n#####";
    let map = parse_map_input(input).unwrap();
    assert_eq!(map.len(), 5);
    assert_eq!(map[0].len(), 5);
    assert_eq!(map[1][1], 'S');
    assert_eq!(map[2][2], '#');
}

#[test]
fn test_parse_map_input_empty() {
    let input = "";
    assert!(parse_map_input(input).is_err());
}

#[test]
fn test_parse_map_input_whitespace_only() {
    let input = "\n   \n\t\n";
    assert!(parse_map_input(input).is_err());
}

#[test]
fn test_parse_map_input_inconsistent_rows() {
    let input = "###\n#S.#\n####";
    assert!(parse_map_input(input).is_err());
}

#[test]
fn test_find_start_found() {
    let map: Map = vec![
        vec!['#', '#', '#'],
        vec!['#', 'S', '.'],
        vec!['#', '.', '#'],
    ];
    assert_eq!(find_start(&map), Some((1, 1)));
}

#[test]
fn test_find_start_not_found() {
    let map: Map = vec![
        vec!['#', '#', '#'],
        vec!['#', '.', '.'],
        vec!['#', '.', '#'],
    ];
    assert_eq!(find_start(&map), None);
}

#[test]
fn test_calculate_echo_distance_north() {
    let map: Map = vec![
        vec!['#', '#', '#', '#', '#'],
        vec!['#', 'S', '.', '.', '#'],
        vec!['#', '.', '#', '.', '#'],
        vec!['#', '.', '.', '.', '#'],
        vec!['#', '#', '#', '#', '#'],
    ];
    // S at (1,1)
    assert_eq!(calculate_echo_distance(&map, 1, 1, -1, 0), 1); // North to #
}

#[test]
fn test_calculate_echo_distance_south() {
    let map: Map = vec![
        vec!['#', '#', '#', '#', '#'],
        vec!['#', 'S', '.', '.', '#'],
        vec!['#', '.', '#', '.', '#'],
        vec!['#', '.', '.', '.', '#'],
        vec!['#', '#', '#', '#', '#'],
    ];
    // S at (1,1)
    assert_eq!(calculate_echo_distance(&map, 1, 1, 1, 0), 2); // South to # (at (3,1))
}

#[test]
fn test_calculate_echo_distance_east() {
    let map: Map = vec![
        vec!['#', '#', '#', '#', '#'],
        vec!['#', 'S', '.', '.', '#'],
        vec!['#', '.', '#', '.', '#'],
        vec!['#', '.', '.', '.', '#'],
        vec!['#', '#', '#', '#', '#'],
    ];
    // S at (1,1)
    assert_eq!(calculate_echo_distance(&map, 1, 1, 0, 1), 3); // East to # (at (1,4))
}

#[test]
fn test_calculate_echo_distance_west() {
    let map: Map = vec![
        vec!['#', '#', '#', '#', '#'],
        vec!['#', 'S', '.', '.', '#'],
        vec!['#', '.', '#', '.', '#'],
        vec!['#', '.', '.', '.', '#'],
        vec!['#', '#', '#', '#', '#'],
    ];
    // S at (1,1)
    assert_eq!(calculate_echo_distance(&map, 1, 1, 0, -1), 1); // West to #
}

#[test]
fn test_calculate_echo_distance_boundary_only() {
    let map: Map = vec![
        vec!['S', '.', '.'],
        vec!['.', '.', '.'],
        vec!['.', '.', '.'],
    ];
    // S at (0,0)
    assert_eq!(calculate_echo_distance(&map, 0, 0, -1, 0), 1); // North to boundary
    assert_eq!(calculate_echo_distance(&map, 0, 0, 0, -1), 1); // West to boundary
    assert_eq!(calculate_echo_distance(&map, 0, 0, 1, 0), 1); // South to .
    assert_eq!(calculate_echo_distance(&map, 0, 0, 0, 1), 1); // East to .
}

#[test]
fn test_calculate_echo_distance_no_obstacle_in_direction() {
    let map: Map = vec![
        vec!['#', '#', '#'],
        vec!['S', '.', '.'],
        vec!['#', '#', '#'],
    ];
    // S at (1,0)
    assert_eq!(calculate_echo_distance(&map, 1, 0, 0, 1), 3); // East to boundary
}

#[test]
fn test_integration_simple_map() {
    let input = "#####\n#S..#\n#.#.#\n#...#\n#####";
    let map = parse_map_input(input).unwrap();
    let (start_row, start_col) = find_start(&map).unwrap();

    assert_eq!(start_row, 1);
    assert_eq!(start_col, 1);

    assert_eq!(calculate_echo_distance(&map, start_row, start_col, -1, 0), 1); // North
    assert_eq!(calculate_echo_distance(&map, start_row, start_col, 1, 0), 2);  // South
    assert_eq!(calculate_echo_distance(&map, start_row, start_col, 0, 1), 3);  // East
    assert_eq!(calculate_echo_distance(&map, start_row, start_col, 0, -1), 1); // West
}

#[test]
fn test_integration_open_map() {
    let input = "...\n.S.\n...";
    let map = parse_map_input(input).unwrap();
    let (start_row, start_col) = find_start(&map).unwrap();

    assert_eq!(start_row, 1);
    assert_eq!(start_col, 1);

    assert_eq!(calculate_echo_distance(&map, start_row, start_col, -1, 0), 2); // North to boundary
    assert_eq!(calculate_echo_distance(&map, start_row, start_col, 1, 0), 2);  // South to boundary
    assert_eq!(calculate_echo_distance(&map, start_row, start_col, 0, 1), 2);  // East to boundary
    assert_eq!(calculate_echo_distance(&map, start_row, start_col, 0, -1), 2); // West to boundary
}

#[test]
fn test_integration_tight_space() {
    let input = "###\n#S#\n###";
    let map = parse_map_input(input).unwrap();
    let (start_row, start_col) = find_start(&map).unwrap();

    assert_eq!(start_row, 1);
    assert_eq!(start_col, 1);

    assert_eq!(calculate_echo_distance(&map, start_row, start_col, -1, 0), 1); // North
    assert_eq!(calculate_echo_distance(&map, start_row, start_col, 1, 0), 1);  // South
    assert_eq!(calculate_echo_distance(&map, start_row, start_col, 0, 1), 1);  // East
    assert_eq!(calculate_echo_distance(&map, start_row, start_col, 0, -1), 1); // West
}
