#[cfg(test)]
mod tests {
    use radiation_safe::filter_safe_locations;

    #[test]
    fn test_basic_filtering() {
        let data = "Vault:12\nWasteland:85\nOasis:30";
        let result = filter_safe_locations(40, data);
        assert_eq!(result, vec!["Vault".to_string(), "Oasis".to_string()]);
    }

    #[test]
    fn test_malformed_lines_are_ignored() {
        let data = "BadLine\nGood:20\nAlsoBad:xyz\nSafe:15";
        let result = filter_safe_locations(25, data);
        assert_eq!(result, vec!["Good".to_string(), "Safe".to_string()]);
    }

    #[test]
    fn test_no_safe_locations() {
        let data = "Hot:100\nScorch:90";
        let result = filter_safe_locations(50, data);
        assert!(result.is_empty());
    }
}
