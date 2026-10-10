// Mock rationale: The test verifies that the ASCII output dimensions match the QR matrix size.
// It does not depend on external resources and runs entirely offline.

use qr_code_artist::encode_to_ascii;
use qrcode::QrCode;

#[test]
fn test_output_dimensions() {
    let text = "Test";
    // Generate the QR code to obtain its matrix size.
    let code = QrCode::new(text).expect("Failed to create QR code");
    let size = code.width(); // number of modules per side

    let out = encode_to_ascii(text);
    // Trim the trailing newline for accurate line counting.
    let lines: Vec<&str> = out.trim_end().split('\n').collect();
    assert_eq!(lines.len(), size, "Number of output lines should equal QR size");
    for line in lines {
        // Each module is rendered as two characters ("██" or "  ").
        assert_eq!(line.len(), size * 2, "Each line length should be twice the QR size");
    }
}
