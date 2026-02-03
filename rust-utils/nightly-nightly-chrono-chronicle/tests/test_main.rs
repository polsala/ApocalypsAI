#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_known_date() {
        // "2023-01-01" -> sum = 483 -> 483 % 6 = 3
        let date = "2023-01-01";
        let event = generate_event(date);
        assert_eq!(event, "Radioactive rain sang lullabies");
    }

    #[test]
    fn test_another_date() {
        // "1999-12-31" -> compute sum manually
        let date = "1999-12-31";
        // bytes: 49+57+57+57+45+49+50+45+51+49 = 492
        // 492 % 6 = 0
        let event = generate_event(date);
        assert_eq!(event, "Solar flares turned the sky crimson");
    }
}
