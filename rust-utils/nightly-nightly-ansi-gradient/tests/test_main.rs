#[cfg(test)]
mod tests {
    use super::*;
    use ansi_gradient::gradient;

    #[test]
    fn test_gradient_simple() {
        let input = "ABC";
        let output = gradient(input);
        // Expected sequence: red A, orange B, yellow C, then reset.
        let expected = format!("{}A{}B{}C\x1b[0m", "\x1b[31m", "\x1b[33m", "\x1b[33m");
        assert_eq!(output, expected);
    }

    #[test]
    fn test_gradient_wraps_colors() {
        let input = "ABCDEFGH"; // 8 chars, 7 colors -> last char repeats first color
        let output = gradient(input);
        // The 8th character should be colored with the first color (red).
        assert!(output.contains("\x1b[31mH"));
    }
}
