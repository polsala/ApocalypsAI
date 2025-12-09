pub fn rainbow(text: &str) -> String {
    let colors = [31, 33, 32, 36, 34, 35];
    let mut result = String::new();
    for (i, ch) in text.chars().enumerate() {
        let color = colors[i % colors.len()];
        result.push_str(&format!("\x1b[{}m{}\x1b[0m", color, ch));
    }
    result
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_rainbow_basic() {
        let input = "ABC";
        let expected = "\x1b[31mA\x1b[0m\x1b[33mB\x1b[0m\x1b[32mC\x1b[0m";
        assert_eq!(rainbow(input), expected);
    }
}
