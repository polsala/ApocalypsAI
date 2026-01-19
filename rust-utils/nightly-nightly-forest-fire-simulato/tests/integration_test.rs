#[cfg(test)]
mod tests {
    use super::*;
    use rand::SeedableRng;
    use rand::rngs::StdRng;

    #[test]
    fn test_initialisation_is_deterministic() {
        // Fixed seed should produce the same initial grid every time
        let seed = 12345u64;
        let mut rng1 = StdRng::seed_from_u64(seed);
        let mut rng2 = StdRng::seed_from_u64(seed);
        let forest1 = Forest::new(5, 5, &mut rng1);
        let forest2 = Forest::new(5, 5, &mut rng2);
        assert_eq!(forest1.grid, forest2.grid);
    }

    #[test]
    fn test_step_spreads_fire() {
        // Create a tiny 3x3 forest with a single burning cell in the centre
        let mut grid = vec![
            vec![Cell::Tree, Cell::Tree, Cell::Tree],
            vec![Cell::Tree, Cell::Burning, Cell::Tree],
            vec![Cell::Tree, Cell::Tree, Cell::Tree],
        ];
        let mut forest = Forest { width: 3, height: 3, grid };
        let mut rng = StdRng::seed_from_u64(0);
        // Run one step – all neighbours should now be burning (no spontaneous ignitions due to low prob)
        forest.step(&mut rng);
        // Expected pattern after one step
        let expected = vec![
            vec![Cell::Burning, Cell::Burning, Cell::Burning],
            vec![Cell::Burning, Cell::Empty,   Cell::Burning],
            vec![Cell::Burning, Cell::Burning, Cell::Burning],
        ];
        assert_eq!(forest.grid, expected);
    }
}
