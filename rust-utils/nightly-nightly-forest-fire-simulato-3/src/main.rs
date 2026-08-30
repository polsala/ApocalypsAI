use rand::prelude::*;
use std::env;

#[derive(Clone, Copy, PartialEq)]
enum Cell {
    Empty,
    Tree,
    Burning,
}

impl Cell {
    fn to_char(self) -> char {
        match self {
            Cell::Empty => '.',
            Cell::Tree => '🌲',
            Cell::Burning => '🔥',
        }
    }
}

fn init_grid(width: usize, height: usize, tree_density: f64, rng: &mut impl Rng) -> Vec<Vec<Cell>> {
    (0..height)
        .map(|_| {
            (0..width)
                .map(|_| {
                    if rng.gen::<f64>() < tree_density {
                        Cell::Tree
                    } else {
                        Cell::Empty
                    }
                })
                .collect()
        })
        .collect()
}

fn step(grid: &mut Vec<Vec<Cell>>, lightning_prob: f64, rng: &mut impl Rng) {
    let height = grid.len();
    let width = grid[0].len();
    let mut next = grid.clone();

    for y in 0..height {
        for x in 0..width {
            match grid[y][x] {
                Cell::Burning => {
                    next[y][x] = Cell::Empty; // burned out
                }
                Cell::Tree => {
                    // Check neighbors for fire
                    let mut on_fire = false;
                    for dy in -1i32..=1 {
                        for dx in -1i32..=1 {
                            if dx == 0 && dy == 0 { continue; }
                            let nx = x as i32 + dx;
                            let ny = y as i32 + dy;
                            if nx >= 0 && nx < width as i32 && ny >= 0 && ny < height as i32 {
                                if grid[ny as usize][nx as usize] == Cell::Burning {
                                    on_fire = true;
                                }
                            }
                        }
                    }
                    if on_fire || rng.gen::<f64>() < lightning_prob {
                        next[y][x] = Cell::Burning;
                    }
                }
                Cell::Empty => {}
            }
        }
    }
    *grid = next;
}

fn print_grid(grid: &Vec<Vec<Cell>>) {
    for row in grid {
        let line: String = row.iter().map(|c| c.to_char()).collect();
        println!("{}", line);
    }
}

fn parse_arg<T: std::str::FromStr>(arg: Option<String>, name: &str) -> T {
    arg.unwrap_or_else(|| {
        eprintln!("Missing argument: {}", name);
        std::process::exit(1);
    })
    .parse()
    .unwrap_or_else(|_| {
        eprintln!("Invalid value for {}", name);
        std::process::exit(1);
    })
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let width: usize = parse_arg(args.get(0).cloned(), "width");
    let height: usize = parse_arg(args.get(1).cloned(), "height");
    let steps: usize = parse_arg(args.get(2).cloned(), "steps");
    let tree_density: f64 = parse_arg(args.get(3).cloned(), "tree_density");
    let lightning_prob: f64 = parse_arg(args.get(4).cloned(), "lightning_prob");

    // Seed RNG with a deterministic value derived from parameters for reproducibility
    let seed: u64 = (width as u64) ^ ((height as u64) << 16) ^ ((steps as u64) << 32);
    let mut rng = StdRng::seed_from_u64(seed);

    let mut grid = init_grid(width, height, tree_density, &mut rng);
    // Ignite a random tree to start the fire (if any)
    for y in 0..height {
        for x in 0..width {
            if grid[y][x] == Cell::Tree {
                grid[y][x] = Cell::Burning;
                break;
            }
        }
        break;
    }

    for step_num in 0..steps {
        println!("Step {}:", step_num + 1);
        print_grid(&grid);
        println!();
        step(&mut grid, lightning_prob, &mut rng);
    }
}
