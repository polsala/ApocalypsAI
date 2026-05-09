#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hint_determinism() {
        // Same direction and seed must always produce the same hint
        let hint1 = generate_hint("N", 42);
        let hint2 = generate_hint("N", 42);
        assert_eq!(hint1, hint2);
    }

    #[test]
    fn test_different_seeds_change_hint() {
        let hint_a = generate_hint("E", 1);
        let hint_b = generate_hint("E", 2);
        assert_ne!(hint_a, hint_b);
    }

    #[test]
    fn test_invalid_direction_handling() {
        // The generate_hint function assumes a valid direction; this test ensures
        // that the CLI layer validates input, not the generator itself.
        // Here we simply verify that calling with an unexpected direction still
        // returns a string (no panic).
        let hint = generate_hint("X", 0);
        assert!(hint.contains("compass"));
    }
}
