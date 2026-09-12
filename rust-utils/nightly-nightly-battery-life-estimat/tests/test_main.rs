#[cfg(test)]
mod tests {
    use super::super::lib;

    #[test]
    fn test_estimate_normal() {
        let hours = lib::estimate_hours(2000.0, 500.0);
        assert_eq!(hours, 4.0);
    }

    #[test]
    fn test_estimate_zero_draw() {
        let hours = lib::estimate_hours(1000.0, 0.0);
        assert!(hours.is_infinite());
    }

    #[test]
    fn test_parse_valid() {
        assert_eq!(lib::parse_arg("123.45").unwrap(), 123.45);
    }

    #[test]
    fn test_parse_invalid() {
        assert!(lib::parse_arg("not-a-number").is_err());
    }
}
