use nightly_qr_code_cli::generate_qr;

#[test]
fn test_qr_contains_blocks() {
    let qr = generate_qr("test");
    // The rendered QR should contain Unicode block characters and newlines
    assert!(qr.contains('█'));
    assert!(qr.contains('\n'));
}
