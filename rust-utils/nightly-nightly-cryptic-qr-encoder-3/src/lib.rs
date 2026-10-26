use qrcode::QrCode;
use qrcode::render::unicode;

/// Encode the given text into an ASCII QR code using Unicode dense blocks.
///
/// Returns a `String` containing the rendered QR code where the dark modules are
/// represented by the `█` character and light modules by a space. Newlines separate rows.
pub fn encode_to_ascii(text: &str) -> String {
    let code = QrCode::new(text.as_bytes()).expect("Failed to create QR code");
    code.render::<unicode::Dense1x2>()
        .quiet_zone(false)
        .build()
}
