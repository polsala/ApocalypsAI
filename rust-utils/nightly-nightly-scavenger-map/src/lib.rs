use rand::prelude::*;

/// Generate a random ASCII map.
///
/// * `width` – number of columns.
/// * `height` – number of rows.
/// * `resources` – slice of single‑character symbols to place on the map.
/// * `seed` – deterministic seed for the RNG.
///
/// Returns a vector of strings, each representing a row.
pub fn generate_map(width: usize, height: usize, resources: &[char], seed: u64) -> Vec<String> {
    // Initialise empty grid filled with '.'
    let mut grid: Vec<Vec<char>> = vec![vec['.'; width]; height];

    let mut rng = StdRng::seed_from_u64(seed);
    let mut empty_cells: Vec<(usize, usize)> = (0..height)
        .flat_map(|y| (0..width).map(move |x| (y, x)))
        .collect();

    for &res in resources {
        if empty_cells.is_empty() {
            break; // no space left
        }
        let idx = rng.gen_range(0..empty_cells.len());
        let (y, x) = empty_cells.swap_remove(idx);
        grid[y][x] = res;
    }

    grid.into_iter()
        .map(|row| row.into_iter().collect())
        .collect()
}
