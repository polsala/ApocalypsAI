#[cfg(test)]
mod tests {
    use nightly_cryptic_qr_encoder::render_qr_ascii;

    #[test]
    fn test_ascii_characters() {
        let ascii = render_qr_ascii("test");
        // Ensure the output only contains the expected Unicode block characters and newlines.
        for ch in ascii.chars() {
            if ch != '\n' {
                assert!(ch == '█' || ch == '░', "Unexpected character in QR output: {}", ch);
            }
        }
        assert!(!ascii.is_empty(), "QR output should not be empty");
    }
}
