#[cfg(test)]
mod tests {
    use super::super::generate_route;

    #[test]
    fn test_repeatability() {
        let locations = vec![
            "A".to_string(),
            "B".to_string(),
            "C".to_string(),
            "D".to_string(),
        ];
        let seed = 12345u64;
        let route1 = generate_route(locations.clone(), seed);
        let route2 = generate_route(locations, seed);
        // The two runs with the same seed must produce identical output
        assert_eq!(route1, route2);
        // First location distance should be zero
        assert_eq!(route1[0].1, 0);
        // All subsequent distances must be within 1..=10 km
        for (_, dist) in route1.iter().skip(1) {
            assert!(*dist >= 1 && *dist <= 10);
        }
    }
}
