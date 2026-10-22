use qrcode::QrCode;
use qrcode::render::unicode;

/// Generates an ASCII representation of a QR code for the given `data`.
///
/// The output uses the `Dense1x2` Unicode renderer, which draws the QR
/// code with `█` for dark modules and a space for light modules.
pub fn generate_qr_ascii(data: &str) -> String {
    let code = QrCode::new(data.as_bytes()).expect("Failed to create QR code");
    code.render::<unicode::Dense1x2>()
        .quiet_zone(false)
        .build()
}
