use qrcode::QrCode;
use qrcode::render::unicode;

/// Generate an ASCII representation of a QR code for the given data.
///
/// Each QR module is rendered as two characters:
/// * `█` for a dark module
/// * space (` `) for a light module
///
/// The function returns a string where rows are separated by `\n`.
pub fn generate_qr_ascii(data: &str) -> String {
    // Create the QR code (error correction level defaults to Medium)
    let code = QrCode::new(data.as_bytes()).expect("Failed to create QR code");
    // Render the QR code into a matrix of booleans (true = dark)
    let matrix: Vec<Vec<bool>> = code.render::<bool>().quiet_zone(false).build();
    // Convert the boolean matrix into an ASCII string
    let mut lines = Vec::new();
    for row in matrix {
        let mut line = String::new();
        for module in row {
            if module {
                line.push_str("██");
            } else {
                line.push_str("  ");
            }
        }
        lines.push(line);
    }
    lines.join("\n")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ascii_properties() {
        let ascii = generate_qr_ascii("HELLO");
        // Trim trailing newline for analysis
        let trimmed = ascii.trim_end();
        let rows: Vec<&str> = trimmed.split('\n').collect();
        assert!(!rows.is_empty(), "QR output should have at least one row");
        let height = rows.len();
        // All rows must have the same length
        let width = rows[0].len();
        for row in &rows {
            assert_eq!(row.len(), width, "All rows must be equal width");
            // Width must be even because each module is two characters
            assert_eq!(width % 2, 0, "Row width must be even");
            // Only allowed characters are space and the block character
            for ch in row.chars() {
                assert!(ch == ' ' || ch == '█', "Invalid character in QR output");
            }
        }
        // Height should equal width / 2 (since each module is two chars wide)
        assert_eq!(height, width / 2, "QR should be square (accounting for double‑width chars)");
    }
}
