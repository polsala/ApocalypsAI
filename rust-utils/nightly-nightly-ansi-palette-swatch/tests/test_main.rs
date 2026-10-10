#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_color_block_format() {
        let s = color_block(5);
        assert_eq!(s, "\x1b[38;5;5m  5\x1b[0m");
    }

    #[test]
    fn test_color_block_range() {
        // Ensure the function works for the extremes of the 0‑255 range.
        let low = color_block(0);
        let high = color_block(255);
        assert_eq!(low, "\x1b[38;5;0m  0\x1b[0m");
        assert_eq!(high, "\x1b[38;5;255m255\x1b[0m");
    }
}
