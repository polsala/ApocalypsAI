#[cfg(test)]
mod tests {
    use nightly_entropy_analyzer::compute_entropy;

    #[test]
    fn test_empty_string() {
        assert_eq!(compute_entropy(""), 0.0);
    }

    #[test]
    fn test_all_same_character() {
        assert_eq!(compute_entropy("aaaa"), 0.0);
    }

    #[test]
    fn test_all_unique_characters() {
        let ent = compute_entropy("abcd");
        assert!((ent - 2.0).abs() < 1e-6);
    }

    #[test]
    fn test_mixed_frequencies() {
        // "abca" -> a:2, b:1, c:1 => entropy = 1.5 bits
        let ent = compute_entropy("abca");
        assert!((ent - 1.5).abs() < 1e-6);
    }
}
