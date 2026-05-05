use nightly_qr_ascii_art::generate_qr_ascii;

#[test]
fn test_qr_dimensions() {
    // "HELLO" fits in a Version‑1 QR (21×21 modules) with low error correction.
    let out = generate_qr_ascii("HELLO");
    let lines: Vec<&str> = out.lines().collect();
    assert_eq!(lines.len(), 21, "QR should have 21 rows");
    for line in lines {
        assert_eq!(line.len(), 42, "Each row should be 21 modules × 2 chars");
    }
}
