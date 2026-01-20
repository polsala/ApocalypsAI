use rand::prelude::*;
use std::env;
use std::fmt;
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Clone, Copy, PartialEq)]
enum Cell {
    Empty,
    Tree,
    Burning,
}

impl fmt::Display for Cell {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let ch = match self {
            Cell::Empty => ' ',
            Cell::Tree => '🌲',
            Cell::Burning => '🔥',
        };
        write!(f, "{}", ch)
    }
}

struct Forest {
    width: usize,
    height: usize,
    grid: Vec<Vec<Cell>>, // row‑major
}

impl Forest {
    fn new(width: usize, height: usize, rng: &mut StdRng) -> Self {
        let mut grid = vec![vec![Cell::Empty; width]; height];
        for y in 0..height {
            for x in 0..width {
                // 80% chance of a tree, 20% empty
                let roll: f64 = rng.gen();
                grid[y][x] = if roll < 0.8 { Cell::Tree } else { Cell::Empty };
            }
        }
        // Ignite a random tree to start the fire
        let mut ignited = false;
        while !ignited {
            let x = rng.gen_range(0..width);
            let y = rng.gen_range(0..height);
            if grid[y][x] == Cell::Tree {
                grid[y][x] = Cell::Burning;
                ignited = true;
            }
        }
        Forest { width, height, grid }
    }

    fn step(&mut self, rng: &mut StdRng) -> bool {
        let mut next = self.grid.clone();
        let mut any_burning = false;
        for y in 0..self.height {
            for x in 0..self.width {
                match self.grid[y][x] {
                    Cell::Burning => {
                        next[y][x] = Cell::Empty;
                    }
                    Cell::Tree => {
                        // Check neighbours for fire
                        let mut neighbor_on_fire = false;
                        for dy in -1i32..=1 {
                            for dx in -1i32..=1 {
                                if dy == 0 && dx == 0 { continue; }
                                let ny = y as i32 + dy;
                                let nx = x as i32 + dx;
                                if ny >= 0 && ny < self.height as i32 && nx >= 0 && nx < self.width as i32 {
                                    if self.grid[ny as usize][nx as usize] == Cell::Burning {
                                        neighbor_on_fire = true;
                                    }
                                }
                            }
                        }
                        // Spontaneous ignition probability
                        let spontaneous: f64 = rng.gen();
                        if neighbor_on_fire || spontaneous < 0.001 {
                            next[y][x] = Cell::Burning;
                            any_burning = true;
                        } else {
                            next[y][x] = Cell::Tree;
                        }
                    }
                    Cell::Empty => {
                        next[y][x] = Cell::Empty;
                    }
                }
            }
        }
        self.grid = next;
        // Determine if any cell is burning after this step
        for row in &self.grid {
            if row.iter().any(|&c| c == Cell::Burning) {
                any_burning = true;
                break;
            }
        }
        any_burning
    }

    fn display(&self) {
        for row in &self.grid {
            let line: String = row.iter().map(|c| c.to_string()).collect();
            println!("{}", line);
        }
    }
}

fn parse_arg(arg: &str, name: &str) -> Option<usize> {
    if arg.starts_with(&format!("--{}=", name)) {
        arg[ (name.len() + 3).. ].parse().ok()
    } else {
        None
    }
}

fn main() {
    // Default parameters
    let mut width = 30usize;
    let mut height = 15usize;
    let mut steps = 100usize;
    let mut seed_opt: Option<u64> = None;

    for arg in env::args().skip(1) {
        if let Some(v) = parse_arg(&arg, "width") { width = v; }
        else if let Some(v) = parse_arg(&arg, "height") { height = v; }
        else if let Some(v) = parse_arg(&arg, "steps") { steps = v; }
        else if arg.starts_with("--seed=") {
            if let Ok(v) = arg[7..].parse() { seed_opt = Some(v); }
        }
    }

    // Initialise RNG
    let seed = seed_opt.unwrap_or_else(|| {
        SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs()
    });
    let mut rng = StdRng::seed_from_u64(seed);

    let mut forest = Forest::new(width, height, &mut rng);
    println!("Initial forest (seed = {}):", seed);
    forest.display();
    println!("---");

    for step in 1..=steps {
        let still_burning = forest.step(&mut rng);
        println!("Step {}:", step);
        forest.display();
        println!("---");
        if !still_burning {
            println!("Fire has extinguished after {} steps.", step);
            break;
        }
    }
}
