use qrcode::QrCode;
use qrcode::EcLevel;

/// Generate a QR code matrix (Vec<Vec<bool>>) for the given data.
/// Returns a square matrix where `true` represents a black module.
pub fn generate_qr_matrix(data: &str) -> Vec<Vec<bool>> {
    // Use low error correction to keep the matrix small.
    let code = QrCode::with_error_correction_level(data.as_bytes(), EcLevel::L)
        .expect("Failed to create QR code");
    // Render as a matrix of booleans without quiet zone.
    code.render::<bool>()
        .quiet_zone(false)
        .build()
}

/// Rotate a square boolean matrix 90° clockwise `times` times.
/// `times` is taken modulo 4.
pub fn rotate_matrix(mut matrix: Vec<Vec<bool>>, times: u8) -> Vec<Vec<bool>> {
    let rotations = (times % 4) as usize;
    for _ in 0..rotations {
        let n = matrix.len();
        let mut new = vec![vec![false; n]; n];
        for i in 0..n {
            for j in 0..n {
                new[j][n - 1 - i] = matrix[i][j];
            }
        }
        matrix = new;
    }
    matrix
}

/// Render a boolean matrix as an ASCII string.
/// Black modules become "██", white modules become "  ".
pub fn render_ascii(matrix: &[Vec<bool>]) -> String {
    let mut out = String::new();
    for row in matrix {
        for &cell in row {
            out.push_str(if cell { "██" } else { "  " });
        }
        out.push('\n');
    }
    out
}
