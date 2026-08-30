#[cfg(test)]
mod tests {
    use super::*;
    use chrono::NaiveDate;

    // Mock rationale: we provide a small CSV string directly; no file I/O or network.
    const MOCK_CSV: &str = "name,quantity,expiration_date\nWater Bottle,10,2025-12-31\nCanned Beans,5,2024-03-15\nRadiated Fruit,2,2023-09-01";

    #[test]
    fn test_parse_items() {
        let items = parse_items(MOCK_CSV).expect("parse should succeed");
        assert_eq!(items.len(), 3);
        assert_eq!(items[0].name, "Water Bottle");
        assert_eq!(items[0].qty, 10);
        assert_eq!(items[0].exp, NaiveDate::from_ymd_opt(2025, 12, 31).unwrap());
    }

    #[test]
    fn test_sort_by_expiration() {
        let items = parse_items(MOCK_CSV).unwrap();
        let sorted = sort_by_expiration(items);
        assert_eq!(sorted[0].name, "Radiated Fruit");
        assert_eq!(sorted[1].name, "Canned Beans");
        assert_eq!(sorted[2].name, "Water Bottle");
    }

    #[test]
    fn test_suggest_use() {
        let items = parse_items(MOCK_CSV).unwrap();
        let sorted = sort_by_expiration(items);
        let suggestion = suggest_use(&sorted).expect("there is at least one item");
        assert_eq!(suggestion.name, "Radiated Fruit");
    }
}
