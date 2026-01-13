#[cfg(test)]
mod tests {
    use super::*;
    use cryptic_qr_generator::generate_qr_ascii;

    #[test]
    fn test_qr_ascii_is_nonempty_and_valid_chars() {
        let out = generate_qr_ascii("hello");
        // Ensure something was produced
        assert!(!out.is_empty(), "Output should not be empty");
        // Only allowed characters (full block, space, newline) should appear
        for ch in out.chars() {
            assert!(ch == 'â' || ch == ' ' || ch == '
', "Unexpected character in output");
        }
        // At least one newline indicates rows were rendered
        assert!(out.contains('
'), "Output should contain newlines");
    }
}

