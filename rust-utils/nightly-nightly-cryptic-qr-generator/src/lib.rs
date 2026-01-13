use qrcode::QrCode;
use qrcode::EcLevel;

/// Generate an ASCII representation of a QR code for the given data.
///
/// The output consists of Unicode fullâblock characters (â) for dark modules
/// and spaces for light modules, terminated by newlines for each row.
pub fn generate_qr_ascii(data: &str) -> String {
    // Create QR code with medium error correction.
    let code = QrCode::with_error_correction_level(data.as_bytes(), EcLevel::M)
        .expect("Failed to create QR code");
    // Render the QR matrix as a 2âD bool vector (true = dark).
    let matrix: Vec<Vec<bool>> = code.render::<bool>()
        .quiet_zone(false)
        .build();
    let mut result = String::new();
    for row in matrix {
        for module in row {
            if module {
                result.push('â');
            } else {
                result.push(' ');
            }
        }
        result.push('
');
    }
    result
}

