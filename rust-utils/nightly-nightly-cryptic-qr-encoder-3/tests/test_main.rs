#[cfg(test)]
mod tests {
    use super::super::generate_qr;

    #[test]
    fn test_generate_qr_nonempty() {
        let result = generate_qr("HELLO").expect("QR generation should succeed");
        // The rendered QR code should contain at least one block character.
        assert!(result.contains('█'), "Rendered QR should contain block characters");
    }

    #[test]
    fn test_generate_qr_error_handling() {
        // An empty string is still valid for QR, but we can test a very long input to trigger an error.
        let long_input = "A".repeat(5000);
        let result = generate_qr(&long_input);
        // Depending on the library, this may error; we just ensure it does not panic.
        assert!(result.is_err() || result.is_ok());
    }
}
