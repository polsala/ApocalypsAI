use cryptic_qr_encoder::encode_to_ascii;

#[test]
fn test_encode_hello() {
    let ascii = encode_to_ascii("HELLO");
    // The output should contain at least one dark block character
    assert!(ascii.contains('█'));
    // The output should not be empty after trimming whitespace
    assert!(!ascii.trim().is_empty());
}
