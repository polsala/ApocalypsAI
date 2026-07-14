#[cfg(test)]
mod tests {
    use super::*;
    use qr_ascii_encoder::encode_to_ascii;

    #[test]
    fn test_ascii_properties() {
        let ascii = encode_to_ascii("test");
        // Ensure output is non‑empty.
        assert!(!ascii.is_empty(), "ASCII output should not be empty");
        // Each line should have an even number of characters (each module is two chars).
        for line in ascii.lines() {
            assert_eq!(line.len() % 2, 0, "Line length must be even");
            // Only allowed characters are the block character and space.
            for ch in line.chars() {
                assert!(ch == '█' || ch == ' ', "Unexpected character '{}' in output", ch);
            }
        }
    }
}
