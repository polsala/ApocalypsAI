use qrcode::QrCode;
use qrcode::render::unicode;

/// Generate an ASCII‑art QR code for the given input string.
///
/// The function returns a `String` containing Unicode block characters
/// that render a scannable QR code when printed to a terminal.
pub fn generate_qr_ascii(data: &str) -> String {
    // Create the QR code matrix; unwrap is safe for short strings.
    let code = QrCode::new(data.as_bytes()).expect("Failed to create QR code");
    // Render using dense 1x2 Unicode characters for a compact representation.
    code.render::<unicode::Dense1x2>()
        .quiet_zone(false)
        .build()
}
