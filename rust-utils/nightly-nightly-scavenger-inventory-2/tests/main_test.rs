use nightly_scavenger_inventory::{Item, prioritize};
use chrono::NaiveDate;

#[test]
fn test_prioritize_external() {
    let items = vec![
        Item {
            name: "First Aid Kit".to_string(),
            quantity: 2,
            expires: NaiveDate::from_ymd_opt(2024, 3, 10).unwrap(),
        },
        Item {
            name: "Bottled Water".to_string(),
            quantity: 8,
            expires: NaiveDate::from_ymd_opt(2023, 9, 5).unwrap(),
        },
    ];
    let sorted = prioritize(&items);
    assert_eq!(sorted[0].name, "Bottled Water");
    assert_eq!(sorted[1].name, "First Aid Kit");
}
