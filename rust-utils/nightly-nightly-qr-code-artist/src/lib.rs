use qrcode::QrCode;
use qrcode::render::unicode;

/// Encode the given text into an ASCII representation of a QR code.
///
/// Dark modules are rendered as `██` and light modules as two spaces.
/// The function returns a string containing newline‑separated rows.
pub fn encode_to_ascii(text: &str) -> String {
    let code = QrCode::new(text).expect("Failed to create QR code");
    code.render::<unicode::Dense1x2>()
        .quiet_zone(false)
        .build()
}
