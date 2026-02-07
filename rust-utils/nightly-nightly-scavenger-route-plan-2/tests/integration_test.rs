#[cfg(test)]
mod tests {
    use nightly_scavenger_route_planner::generate_route;

    #[test]
    fn test_deterministic_route() {
        // Mock input locations (unsorted on purpose).
        let locations = vec![
            "Abandoned Mall",
            "Ruined Library",
            "Old Farm",
            "Collapsed Bridge",
        ];
        // Seed 2 will rotate the alphabetically sorted list left by 2.
        let route = generate_route(&locations, 2);
        let expected = vec![
            "Old Farm",
            "Ruined Library",
            "Abandoned Mall",
            "Collapsed Bridge",
        ];
        assert_eq!(route, expected);
    }
}
