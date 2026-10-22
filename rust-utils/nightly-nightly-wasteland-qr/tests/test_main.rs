use wasteland_qr::generate_qr_ascii;

#[test]
fn test_generate_qr_ascii_nonempty() {
    // The function should always return a non‑empty string for any input.
    let out = generate_qr_ascii("test");
    assert!(!out.is_empty(), "QR output should not be empty");
    // The output must consist only of the expected Unicode block characters,
    // spaces, and newlines.
    assert!(out.chars().all(|c| c == '█' || c == ' ' || c == '\n'));
}
