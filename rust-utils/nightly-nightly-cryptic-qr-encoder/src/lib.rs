use qrcode::QrCode;
use qrcode::render::unicode;

/// Generate an ASCII QR code for the given text.
/// Returns a string where each line ends with a newline character.
pub fn generate_qr_ascii(text: &str) -> String {
    let code = QrCode::new(text.as_bytes()).expect("Failed to create QR code");
    // Use dense Unicode blocks for compact representation
    code.render::<unicode::Dense1x2>()
        .quiet_zone(false)
        .build()
}

/// Wrap the given ASCII QR code in a decorative radiation border.
/// The border uses the â¢ symbol and adds two spaces of padding on each side.
pub fn add_radiation_border(ascii_qr: &str) -> String {
    let lines: Vec<&str> = ascii_qr.lines().collect();
    let width = lines.iter().map(|l| l.chars().count()).max().unwrap_or(0);
    let border = "â¢".repeat(width + 4);
    let mut result = String::new();
    result.push_str(&border);
    result.push('
');
    for line in lines {
        result.push_str(&format!("â¢ {} â¢
", line));
    }
    result.push_str(&border);
    result
}

