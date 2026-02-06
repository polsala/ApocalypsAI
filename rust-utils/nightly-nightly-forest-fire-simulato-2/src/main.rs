use std::env;

#[derive(Clone, Copy, PartialEq, Eq)]
enum Cell {
    Empty,
    Tree,
    Burning,
}

impl Cell {
    fn to_char(self) -> char {
        match self {
            Cell::Empty => ' ',
            Cell::Tree => '🌲',
            Cell::Burning => '🔥',
        }
    }
}

struct Grid {
    width: usize,
    height: usize,
    cells: Vec<Cell>,
}

impl Grid {
    fn new(width: usize, height: usize) -> Self {
        // Start with all trees.
        let cells = vec![Cell::Tree; width * height];
        Grid { width, height, cells }
    }

    fn index(&self, x: usize, y: usize) -> usize {
        y * self.width + x
    }

    fn get(&self, x: isize, y: isize) -> Option<Cell> {
        if x < 0 || y < 0 {
            return None;
        }
        let (x, y) = (x as usize, y as usize);
        if x >= self.width || y >= self.height {
            None
        } else {
            Some(self.cells[self.index(x, y)])
        }
    }

    fn set(&mut self, x: usize, y: usize, value: Cell) {
        let idx = self.index(x, y);
        self.cells[idx] = value;
    }

    fn step(&mut self, rng: &mut Lcg, ignition_chance: u8) {
        let mut next = self.cells.clone();
        for y in 0..self.height {
            for x in 0..self.width {
                let idx = self.index(x, y);
                match self.cells[idx] {
                    Cell::Burning => {
                        // Burning becomes empty.
                        next[idx] = Cell::Empty;
                    }
                    Cell::Tree => {
                        // Check orthogonal neighbours for fire.
                        let neighbours = [
                            (x as isize - 1, y as isize),
                            (x as isize + 1, y as isize),
                            (x as isize, y as isize - 1),
                            (x as isize, y as isize + 1),
                        ];
                        let mut will_burn = false;
                        for (nx, ny) in neighbours.iter() {
                            if let Some(Cell::Burning) = self.get(*nx, *ny) {
                                will_burn = true;
                                break;
                            }
                        }
                        // Spontaneous ignition.
                        if !will_burn {
                            let roll = (rng.next() % 100) as u8;
                            if roll < ignition_chance {
                                will_burn = true;
                            }
                        }
                        if will_burn {
                            next[idx] = Cell::Burning;
                        }
                    }
                    Cell::Empty => {}
                }
            }
        }
        self.cells = next;
    }

    fn render(&self) -> String {
        let mut out = String::new();
        for y in 0..self.height {
            for x in 0..self.width {
                out.push(self.cells[self.index(x, y)].to_char());
            }
            if y + 1 < self.height {
                out.push('\n');
            }
        }
        out
    }
}

// Simple linear congruential generator – deterministic and std‑lib only.
struct Lcg {
    state: u64,
}

impl Lcg {
    fn new(seed: u64) -> Self {
        Lcg { state: seed }
    }

    fn next(&mut self) -> u64 {
        // Constants from Numerical Recipes.
        self.state = self.state.wrapping_mul(6364136223846793005).wrapping_add(1);
        self.state
    }
}

fn parse_arg<T: std::str::FromStr>(arg: Option<&String>, name: &str) -> T {
    arg.expect(&format!("Missing argument: {}", name))
        .parse::<T>()
        .ok()
        .expect(&format!("Invalid value for {}", name))
}

fn main() {
    let args: Vec<String> = env::args().collect();
    // Expected: <width> <height> <steps> [seed]
    let width: usize = parse_arg(args.get(1), "width");
    let height: usize = parse_arg(args.get(2), "height");
    let steps: usize = parse_arg(args.get(3), "steps");
    let seed: u64 = args.get(4).map(|s| s.parse().unwrap_or(0)).unwrap_or(0);

    let mut grid = Grid::new(width, height);
    let mut rng = Lcg::new(seed);
    // Ignite a single random tree to start the fire.
    let start_idx = (rng.next() as usize) % (width * height);
    grid.cells[start_idx] = Cell::Burning;

    println!("Initial state:");
    println!("{}", grid.render());
    for step in 1..=steps {
        grid.step(&mut rng, 5); // 5% spontaneous ignition chance.
        println!("\nStep {}:", step);
        println!("{}", grid.render());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lcg_determinism() {
        let mut rng = Lcg::new(0);
        let first = rng.next();
        let second = rng.next();
        assert_eq!(first, 6364136223846793005);
        assert_eq!(second, 1152921504606846976);
    }

    #[test]
    fn test_step_simple_fire_spread() {
        // 3x3 grid, centre burning, no spontaneous ignition.
        let mut grid = Grid::new(3, 3);
        grid.cells[grid.index(1, 1)] = Cell::Burning;
        let mut rng = Lcg::new(0);
        grid.step(&mut rng, 0);
        // After one step, centre becomes empty, orthogonal neighbours burn.
        let expected = vec![
            Cell::Tree,   Cell::Burning, Cell::Tree,
            Cell::Burning,Cell::Empty,  Cell::Burning,
            Cell::Tree,   Cell::Burning, Cell::Tree,
        ];
        assert_eq!(grid.cells, expected);
    }

    #[test]
    fn test_render_output() {
        let mut grid = Grid::new(2, 2);
        grid.cells[0] = Cell::Tree;
        grid.cells[1] = Cell::Burning;
        grid.cells[2] = Cell::Empty;
        grid.cells[3] = Cell::Tree;
        let rendered = grid.render();
        let expected = format!("{}{}{}{}", '🌲', '🔥', '\n', ' ', '🌲');
        // The expected string is "🌲🔥\n 🌲"
        assert_eq!(rendered, "🌲🔥\n 🌲");
    }
}
