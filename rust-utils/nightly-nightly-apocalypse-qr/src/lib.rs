use qrcode::QrCode;

/// Generate an ASCII representation of a QR code.
///
/// * `data` – the string to encode.
/// * `radiation` – if true, the output is wrapped in a radiation‑symbol border.
///
/// Returns a `String` containing the rendered QR code.
pub fn generate_qr_ascii(data: &str, radiation: bool) -> String {
    // Create the QR code matrix; unwrap is safe for short strings used in tests.
    let code = QrCode::new(data).expect("Failed to create QR code");
    // Render using Unicode block characters for better terminal visibility.
    let ascii = code
        .render()
        .light_color('░')
        .dark_color('█')
        .build();

    if radiation {
        // Build a radiation border: a line of ☢ symbols above and below,
        // and ☢ symbols framing each inner line.
        let inner_width = ascii.lines().next().map(|l| l.chars().count()).unwrap_or(0);
        let border_line = "☢".repeat(inner_width + 4);
        let mut result = String::new();
        result.push_str(&border_line);
        result.push('\n');
        for line in ascii.lines() {
            result.push_str(&format!("☢ {} ☢\n", line));
        }
        result.push_str(&border_line);
        result
    } else {
        ascii
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_radiation_border_structure() {
        let output = generate_qr_ascii("test", true);
        let mut lines = output.lines();
        let first = lines.next().expect("output should have at least one line");
        // The first line must be only radiation symbols.
        assert!(first.chars().all(|c| c == '☢'));
        // The last line should be identical to the first.
        let last = output.lines().last().unwrap();
        assert_eq!(first, last);
        // Each middle line should start and end with a radiation symbol.
        for line in lines.take_while(|l| *l != first) {
            let chars: Vec<char> = line.chars().collect();
            assert_eq!(chars.first().unwrap(), &'☢');
            assert_eq!(chars.last().unwrap(), &'☢');
        }
    }
}
