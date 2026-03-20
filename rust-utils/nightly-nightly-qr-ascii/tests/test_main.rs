#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_qr_ascii_nonempty() {
        // Mock rationale: we verify that the function returns a non‑empty string
        // containing at least one block character, which indicates that rendering
        // succeeded without needing external resources.
        let output = generate_qr_ascii("test");
        assert!(!output.is_empty(), "Output should not be empty");
        assert!(output.contains('█') || output.contains('░'), "Output should contain block characters");
    }
}
