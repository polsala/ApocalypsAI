use qrcode::QrCode;
use qrcode::EcLevel;
use qrcode::Color;

/// Generate an ASCII representation of a QR code.
///
/// * `input` – the string to encode.
/// * Returns a `String` where each QR module is rendered as `██` (dark) or two spaces (light).
pub fn generate_qr_ascii(input: &str) -> String {
    let code = QrCode::with_error_correction_level(input.as_bytes(), EcLevel::L).unwrap();
    let matrix = code.to_colors();
    let mut out = String::new();
    for row in matrix {
        for color in row {
            if color == Color::Dark {
                out.push_str("██");
            } else {
                out.push_str("  ");
            }
        }
        out.push('\n');
    }
    out
}
