#[cfg(test)]
mod tests {
    use super::super::*;

    #[test]
    fn test_low_radiation() {
        let plants = recommend_plants("low");
        assert_eq!(plants, &["Tomato", "Lettuce", "Carrot"]);
    }

    #[test]
    fn test_medium_radiation() {
        let plants = recommend_plants("medium");
        assert_eq!(plants, &["Radish", "Sunflower", "Kale"]);
    }

    #[test]
    fn test_high_radiation() {
        let plants = recommend_plants("high");
        assert_eq!(plants, &["Radish", "Sunflower", "Kale"]);
    }

    #[test]
    fn test_invalid_radiation_returns_empty() {
        let plants = recommend_plants("unknown");
        assert!(plants.is_empty());
    }
}
