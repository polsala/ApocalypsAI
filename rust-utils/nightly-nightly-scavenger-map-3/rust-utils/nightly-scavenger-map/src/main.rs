use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;
use std::env;

const WIDTH: usize = 10;
const HEIGHT: usize = 5;

fn generate_map(items: &[String], seed: u64) -> Vec<Vec<char>> {
    let mut map = vec![vec!['.'; WIDTH]; HEIGHT];
    let mut rng = StdRng::seed_from_u64(seed);
    for item in items {
        let mut placed = false;
        for _ in 0..100 {
            let x = rng.gen_range(0..WIDTH);
            let y = rng.gen_range(0..HEIGHT);
            if map[y][x] == '.' {
                map[y][x] = item.chars().next().unwrap_or('?').to_ascii_uppercase();
                placed = true;
                break;
            }
        }
        if !placed {
            // map full, stop placing further items
            break;
        }
    }
    map
}

fn print_map(map: &[Vec<char>]) {
    for row in map {
        let line: String = row.iter().map(|c| format!("{} ", c)).collect();
        println!("{}", line.trim_end());
    }
}

fn main() {
    // Collect command‑line arguments (skip program name)
    let args: Vec<String> = env::args().skip(1).collect();
    // Fixed seed ensures deterministic output for testing
    let seed = 42u64;
    let map = generate_map(&args, seed);
    print_map(&map);
}
