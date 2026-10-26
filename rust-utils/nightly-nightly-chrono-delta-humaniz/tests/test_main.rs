#[cfg(test)]
mod tests {
    use super::super::compute_delta;

    #[test]
    fn test_basic_delta() {
        let start = "2023-01-01T00:00:00Z";
        let end = "2023-01-02T03:04:05Z";
        let out = compute_delta(start, end);
        assert_eq!(out, "1 day, 3 hours, 4 minutes, 5 seconds");
    }

    #[test]
    fn test_reverse_order() {
        let start = "2023-01-02T03:04:05Z";
        let end = "2023-01-01T00:00:00Z";
        let out = compute_delta(start, end);
        assert_eq!(out, "1 day, 3 hours, 4 minutes, 5 seconds");
    }

    #[test]
    fn test_same_timestamp() {
        let ts = "2023-05-05T12:30:30Z";
        let out = compute_delta(ts, ts);
        assert_eq!(out, "0 seconds");
    }
}
