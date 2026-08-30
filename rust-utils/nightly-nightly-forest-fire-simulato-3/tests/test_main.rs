#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;
    use rand::rngs::StdRng;

    #[test]
    fn test_initialization_respects_density() {
        let mut rng = StdRng::seed_from_u64(42);
        let grid = init_grid(10, 5, 1.0, &mut rng);
        // With density 1.0 every cell should be a tree
        for row in grid {
            for cell in row {
                assert_eq!(cell, Cell::Tree);
            }
        }
    }

    #[test]
    fn test_step_spreads_fire_to_adjacent_tree() {
        // Create a 3x3 grid with a burning cell in the center and a tree to the right
        let mut grid = vec![
            vec![Cell::Empty, Cell::Empty, Cell::Empty],
            vec![Cell::Empty, Cell::Burning, Cell::Tree],
            vec![Cell::Empty, Cell::Empty, Cell::Empty],
        ];
        let mut rng = StdRng::seed_from_u64(0);
        step(&mut grid, 0.0, &mut rng);
        // After one step, the burning cell becomes empty and the tree becomes burning
        assert_eq!(grid[1][1], Cell::Empty);
        assert_eq!(grid[1][2], Cell::Burning);
    }

    #[test]
    fn test_lightning_ignites_tree() {
        let mut grid = vec![vec![Cell::Tree]];
        let mut rng = StdRng::seed_from_u64(0);
        // With lightning_prob = 1.0 the tree should ignite regardless of neighbors
        step(&mut grid, 1.0, &mut rng);
        assert_eq!(grid[0][0], Cell::Burning);
    }
}
