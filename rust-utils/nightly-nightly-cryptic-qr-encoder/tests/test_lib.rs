#[cfg(test)]
mod tests {
    use super::super::lib;

    #[test]
    fn test_generate_nonempty() {
        let out = lib::generate_qr_ascii("HELLO");
        // The QR code should contain at least one newline and not be empty
        assert!(!out.is_empty(), "QR output should not be empty");
        assert!(out.contains('
'), "QR output should contain line breaks");
    }

    #[test]
    fn test_radiation_border_structure() {
        let base = lib::generate_qr_ascii("HELLO");
        let bordered = lib::add_radiation_border(&base);
        let lines: Vec<&str> = bordered.lines().collect();
        // First and last lines are the full border and must start with â¢
        assert_eq!(lines.first().unwrap().chars().next().unwrap(), 'â¢');
        assert_eq!(lines.last().unwrap().chars().next().unwrap(), 'â¢');
        // Middle lines must start and end with â¢
        for line in &lines[1..lines.len() - 1] {
            let chars: Vec<char> = line.chars().collect();
            assert_eq!(chars[0], 'â¢');
            assert_eq!(chars[chars.len() - 1], 'â¢');
        }
    }
}

