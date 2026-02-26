#[cfg(test)]
mod tests {
    use qr_code_cli::generate_qr_ascii;

    #[test]
    fn generates_nonempty_output() {
        let input = "Hello, world!";
        let qr = generate_qr_ascii(input);
        // The output should not be empty.
        assert!(!qr.is_empty(), "QR output is empty");
        // It should contain at least one dark block character.
        assert!(qr.contains('█'), "QR output does not contain expected block characters");
    }

    #[test]
    fn consistent_output_for_same_input() {
        let input = "ApocalypsAI";
        let first = generate_qr_ascii(input);
        let second = generate_qr_ascii(input);
        // Mock rationale: the QR generation is deterministic, so both strings must match.
        assert_eq!(first, second, "QR generation is not deterministic for identical input");
    }
}
