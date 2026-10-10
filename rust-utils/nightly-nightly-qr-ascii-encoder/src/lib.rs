use qrcode::QrCode;
use qrcode::EcLevel;

/// Encode the given text into a QR code rendered as ASCII art.
///
/// Dark modules are rendered as `██` and light modules as two spaces.
pub fn encode_to_ascii(text: &str) -> String {
    // Generate QR code with medium error correction.
    let code = QrCode::with_error_correction_level(text.as_bytes(), EcLevel::M).unwrap();
    let matrix = code.into_colors();
    let mut result = String::new();
    for row in matrix {
        for &color in row.iter() {
            let block = if color { "██" } else { "  " };
            result.push_str(block);
        }
        result.push('\n');
    }
    result
}
