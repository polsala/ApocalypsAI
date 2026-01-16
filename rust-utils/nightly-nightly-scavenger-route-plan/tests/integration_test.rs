#[cfg(test)]
mod tests {
    use super::super::generate_route;

    #[test]
    fn test_reverse_route() {
        let input = vec!["Base".to_string(), "Warehouse".to_string(), "Outpost".to_string()];
        let result = generate_route(input.clone(), false);
        let expected = vec!["Outpost".to_string(), "Warehouse".to_string(), "Base".to_string()];
        assert_eq!(result, expected);
    }

    #[test]
    fn test_shuffle_route_feature_disabled_falls_back_to_reverse() {
        let input = vec!["A".to_string(), "B".to_string(), "C".to_string()];
        // Even if shuffle flag is true, without the feature it should reverse.
        let result = generate_route(input.clone(), true);
        let expected = vec!["C".to_string(), "B".to_string(), "A".to_string()];
        assert_eq!(result, expected);
    }
}
