use std::{env, fmt::Write as FmtWrite};

use rand::{seq::SliceRandom, Rng, SeedableRng};
use rand::rngs::StdRng;

fn main() {
    // Parse commandâline arguments
    let args: Vec<String> = env::args().collect();
    if args.len() < 4 {
        eprintln!("Usage: {} <width> <height> <resources> [seed]", args[0]);
        eprintln!("  width,height: map dimensions (positive integers)");
        eprintln!("  resources: commaâseparated list of singleâcharacter symbols, e.g. "F,W,R"");
        eprintln!("  seed (optional): integer seed for reproducible maps");
        std::process::exit(1);
    }
    let width: usize = args[1].parse().expect("Invalid width");
    let height: usize = args[2].parse().expect("Invalid height");
    let resources: Vec<char> = args[3]
        .split(',')
        .map(|s| s.trim().chars().next().unwrap())
        .collect();
    let seed: u64 = if args.len() > 4 {
        args[4].parse().expect("Invalid seed")
    } else {
        // Random seed when not supplied
        rand::thread_rng().gen()
    };
    let map = generate_map(width, height, &resources, seed);
    println!("{}", map);
}

/// Generates an ASCII map.
///
/// * `width` â number of columns
/// * `height` â number of rows
/// * `resources` â slice of symbols to scatter
/// * `seed` â RNG seed for deterministic output
pub fn generate_map(width: usize, height: usize, resources: &[char], seed: u64) -> String {
    let mut rng = StdRng::seed_from_u64(seed);
    let mut grid = vec![vec!['.'; width]; height];
    // Place resources in roughly 10% of cells (minimum 1)
    let total_cells = width * height;
    let resource_count = std::cmp::max(1, total_cells / 10);
    for _ in 0..resource_count {
        let y = rng.gen_range(0..height);
        let x = rng.gen_range(0..width);
        let &symbol = resources.choose(&mut rng).unwrap();
        grid[y][x] = symbol;
    }
    // Render the grid into a single string
    let mut out = String::new();
    for row in grid {
        for ch in row {
            out.push(ch);
        }
        out.push('
');
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn deterministic_output() {
        let map1 = generate_map(5, 3, &['F', 'W'], 42);
        let map2 = generate_map(5, 3, &['F', 'W'], 42);
        assert_eq!(map1, map2);
    }
    #[test]
    fn resource_count() {
        let width = 10;
        let height = 10;
        let map = generate_map(width, height, &['R'], 123);
        let count = map.chars().filter(|&c| c == 'R').count();
        let expected = (width * height) / 10;
        assert_eq!(count, expected);
    }
}

