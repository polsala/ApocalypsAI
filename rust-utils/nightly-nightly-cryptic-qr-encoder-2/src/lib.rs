use qrcode::QrCode;
use qrcode::render::unicode;

/// Generates an ASCII QR code for the given input string.
///
/// Returns a string containing the QR code rendered with Unicode block characters.
pub fn render_qr_ascii(input: &str) -> String {
    // Create QR code from the input bytes.
    let code = QrCode::new(input.as_bytes()).expect("Failed to create QR code");
    // Render to Unicode using dense 1x2 blocks (█ and ░).
    code.render::<unicode::Dense1x2>()
        .dark_color(unicode::Dense1x2::Dark)
        .light_color(unicode::Dense1x2::Light)
        .build()
}
