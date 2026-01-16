// Mock rationale: These tests validate the duration parsing logic without requiring actual time-based execution.

mod main;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_milliseconds() {
        let result = main::parse_duration("100ms");
        assert_eq!(result.unwrap(), std::time::Duration::from_millis(100));
    }

    #[test]
    fn test_parse_seconds() {
        let result = main::parse_duration("2.5s");
        let expected = std::time::Duration::new(2, 500_000_000);
        assert_eq!(result.unwrap(), expected);
    }

    #[test]
    fn test_parse_minutes() {
        let result = main::parse_duration("3m");
        assert_eq!(result.unwrap(), std::time::Duration::from_secs(180));
    }

    #[test]
    fn test_parse_hours() {
        let result = main::parse_duration("1h");
        assert_eq!(result.unwrap(), std::time::Duration::from_secs(3600));
    }

    #[test]
    fn test_parse_invalid_unit() {
        let result = main::parse_duration("5d");
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_invalid_number() {
        let result = main::parse_duration("abcms");
        assert!(result.is_err());
    }
}
