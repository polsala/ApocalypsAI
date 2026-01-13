#[cfg(test)]
mod tests {
    use super::super::generate_map;
    use std::collections::HashSet;

    #[test]
    fn test_generate_map_dimensions_and_placement() {
        let width = 5;
        let height = 4;
        let resources = vec![
            "water".to_string(),
            "food".to_string(),
            "ammo".to_string(),
        ];
        let seed = 12345u64;

        let map = generate_map(width, height, &resources, seed);
        // Verify dimensions
        assert_eq!(map.len(), height, "Incorrect height");
        assert_eq!(map[0].len(), width, "Incorrect width");

        // Count nonâdot cells â should equal number of resources
        let mut placed = 0;
        for row in &map {
            for &c in row {
                if c != '.' {
                    placed += 1;
                }
            }
        }
        assert_eq!(placed, resources.len(), "Each resource should appear exactly once");

        // Ensure each resource's first letter appears
        let mut expected: HashSet<char> = HashSet::new();
        for r in &resources {
            expected.insert(r.chars().next().unwrap().to_ascii_uppercase());
        }
        for row in &map {
            for &c in row {
                if c != '.' {
                    assert!(expected.contains(&c), "Unexpected symbol on map");
                }
            }
        }
    }
}

