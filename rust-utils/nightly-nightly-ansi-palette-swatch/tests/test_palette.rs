#[cfg(test)]
mod tests {
    use nightly_ansi_palette_swatch::generate_palette;

    #[test]
    fn test_small_range_contains_expected_codes() {
        let out = generate_palette(0, 1);
        // Verify that the ANSI escape sequences for codes 0 and 1 appear
        assert!(out.contains("\x1b[38;5;0m  0\x1b[0m"));
        assert!(out.contains("\x1b[38;5;1m  1\x1b[0m"));
    }

    #[test]
    fn test_start_greater_than_end_returns_empty() {
        // When start > end the iterator yields nothing, resulting in an empty string
        let out = generate_palette(5, 4);
        assert_eq!(out, "");
    }
}
