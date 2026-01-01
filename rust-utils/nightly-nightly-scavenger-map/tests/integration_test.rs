#[cfg(test)]
mod tests {
    use super::*;
    use nightly_scavenger_map::generate_map;

    #[test]
    fn deterministic_map_with_seed() {
        // Mock rationale: using a fixed seed ensures the output is predictable for the test.
        let width = 5;
        let height = 3;
        let resources = vec!['F', 'W'];
        let seed = 42u64;
        let map = generate_map(width, height, &resources, seed);
        let expected = vec![
            "..F..",
            ".....",
            "W....",
        ];
        assert_eq!(map, expected);
    }
}
