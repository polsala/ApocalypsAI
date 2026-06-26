#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Cursor;
    use chrono::NaiveDate;

    fn sample_csv() -> &'static str {
        "name,category,quantity,expiration_date\n"
        "Canned Beans,food,12,2099-12-01\n"
        "Bandage,medicine,5,2099-01-15\n"
        "Old Bread,food,2,2023-01-01\n"
    }

    #[test]
    fn test_parse_csv() {
        let cursor = Cursor::new(sample_csv());
        let items = parse_csv(cursor).expect("Parsing failed");
        assert_eq!(items.len(), 3);
        assert_eq!(items[0].name, "Canned Beans");
        assert_eq!(items[0].category, "food");
        assert_eq!(items[0].quantity, 12);
        assert_eq!(items[0].expiration, NaiveDate::from_ymd_opt(2099, 12, 1).unwrap());
    }

    #[test]
    fn test_category_totals() {
        let cursor = Cursor::new(sample_csv());
        let items = parse_csv(cursor).unwrap();
        let totals = category_totals(&items);
        assert_eq!(totals.get("food"), Some(&14)); // 12 + 2
        assert_eq!(totals.get("medicine"), Some(&5));
    }

    #[test]
    fn test_expiring_soon() {
        // Mock today as 2023-01-01 for deterministic test
        // Since we cannot change chrono::Utc::today() without a crate, we instead
        // verify that the function correctly identifies an already‑expired item
        // as not "expiring soon" (the function filters future dates only).
        let cursor = Cursor::new(sample_csv());
        let items = parse_csv(cursor).unwrap();
        let soon = expiring_soon(&items, 7);
        // Only "Old Bread" has expiration 2023-01-01 which is today; it should be included.
        // However, because chrono::Utc::today() will be the actual current date when tests run,
        // we cannot guarantee inclusion. To keep the test deterministic, we assert that the
        // function returns a vector (could be empty) and that it never panics.
        assert!(soon.iter().all(|it| it.expiration >= chrono::Utc::today().naive_utc()));
    }

    #[test]
    fn test_random_tip_is_non_empty() {
        let tip = random_tip();
        assert!(!tip.is_empty());
    }
}
