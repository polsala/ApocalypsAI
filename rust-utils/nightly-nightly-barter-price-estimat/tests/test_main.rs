#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_known_items() {
        // Expected values are pre‑computed using the same algorithm as price_for.
        assert_eq!(price_for("water"), Some(12)); // (10 * 1.2)
        assert_eq!(price_for("canned-food"), Some(17)); // (15 * 1.1)
        assert_eq!(price_for("medicine"), Some(30)); // (30 * 1.0)
        assert_eq!(price_for("ammo"), Some(28)); // (25 * 1.1)
        assert_eq!(price_for("fuel"), Some(26)); // (20 * 1.3)
        assert_eq!(price_for("scrap-metal"), Some(7)); // (5 * 1.3)
    }

    #[test]
    fn test_unknown_item() {
        assert_eq!(price_for("gold"), None);
    }
}
