/// Generates an ASCII map from a slice of item names.\n///\n/// Each item is represented by the uppercase first character of its name.\n/// The map is a square grid whose side length is the ceiling of the square\n/// root of the number of items. Items are placed row‑wise in the order they\n/// appear in the slice. Empty cells are filled with `.`.\n///\n/// # Examples\n///\n/// ```\n/// let items = vec!["water", "food", "medicine"];\n/// let map = scavenger_map_generator::generate_map(&items);\n/// assert_eq!(map, vec!["WF", "M."]);\n/// ```\npub fn generate_map(items: &[&str]) -> Vec<String> {
    let n = items.len();
    if n == 0 {
        return Vec::new();
    }
    let size = ( (n as f64).sqrt().ceil() as usize);
    let mut grid = vec![vec!['.'; size]; size];
    for (i, item) in items.iter().enumerate() {
        let row = i / size;
        let col = i % size;
        let ch = item.chars().next().unwrap_or('?').to_ascii_uppercase();
        grid[row][col] = ch;
    }
    grid.iter()
        .map(|row| row.iter().collect())
        .collect()
}
