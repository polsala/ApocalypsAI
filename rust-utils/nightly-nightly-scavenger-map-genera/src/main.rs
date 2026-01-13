use rand::{Rng, SeedableRng};
use rand::rngs::StdRng;
use std::env;

/// Parses commandâline arguments.
/// Returns (width, height, resources, seed).
fn parse_args() -> Result<(usize, usize, Vec<String>, u64), String> {
    let mut width: Option<usize> = None;
    let mut height: Option<usize> = None;
    let mut resources: Option<Vec<String>> = None;
    let mut seed: Option<u64> = None;

    let mut args = env::args().skip(1); // skip program name
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--width" => {
                width = args.next().and_then(|v| v.parse().ok());
            }
            "--height" => {
                height = args.next().and_then(|v| v.parse().ok());
            }
            "--resources" => {
                resources = args.next().map(|v| {
                    v.split(',')
                        .map(|s| s.trim().to_string())
                        .filter(|s| !s.is_empty())
                        .collect()
                });
            }
            "--seed" => {
                seed = args.next().and_then(|v| v.parse().ok());
            }
            _ => {
                return Err(format!("Unexpected argument: {}", arg));
            }
        }
    }

    let w = width.ok_or_else(|| "Missing --width".to_string())?;
    let h = height.ok_or_else(|| "Missing --height".to_string())?;
    let res = resources.ok_or_else(|| "Missing --resources".to_string())?;
    let s = seed.unwrap_or_else(|| {
        // If no seed supplied, use a random one based on system time
        use std::time::{SystemTime, UNIX_EPOCH};
        let dur = SystemTime::now().duration_since(UNIX_EPOCH).unwrap();
        dur.as_secs()
    });
    Ok((w, h, res, s))
}

/// Generates a 2âD grid (height Ã width) filled with '.' and the first letter of each resource.
/// The placement is deterministic given the same `seed`.
pub fn generate_map(width: usize, height: usize, resources: &[String], seed: u64) -> Vec<Vec<char>> {
    let mut grid = vec![vec['.'; width]; height];
    let mut rng = StdRng::seed_from_u64(seed);

    for res in resources {
        let symbol = res.chars().next().unwrap().to_ascii_uppercase();
        // Find a random empty cell; retry until we succeed (grid is guaranteed to have enough free cells).
        loop {
            let x = rng.gen_range(0..width);
            let y = rng.gen_range(0..height);
            if grid[y][x] == '.' {
                grid[y][x] = symbol;
                break;
            }
        }
    }
    grid
}

/// Prints the grid to STDOUT.
fn print_map(grid: &[Vec<char>]) {
    for row in grid {
        let line: String = row.iter().collect();
        println!("{}", line);
    }
}

fn main() {
    match parse_args() {
        Ok((width, height, resources, seed)) => {
            let map = generate_map(width, height, &resources, seed);
            print_map(&map);
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            eprintln!("Usage: scavenger-map --width <num> --height <num> --resources <commaâlist> [--seed <num>]");
            std::process::exit(1);
        }
    }
}

