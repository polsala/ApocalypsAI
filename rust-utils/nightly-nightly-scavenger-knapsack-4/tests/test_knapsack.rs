use nightly_scavenger_knapsack::{Item, knapsack};

#[test]
fn test_knapsack_basic() {
    let items = vec![
        Item { name: "water".to_string(), weight: 3, value: 10 },
        Item { name: "canned-food".to_string(), weight: 2, value: 7 },
        Item { name: "first-aid".to_string(), weight: 5, value: 12 },
        Item { name: "radio".to_string(), weight: 1, value: 4 },
    ];
    let selected = knapsack(&items, 5);
    // Optimal selection is canned-food + radio (value 11)
    assert_eq!(selected, vec!["canned-food", "radio"]);
}

#[test]
fn test_knapsack_no_items() {
    let items: Vec<Item> = vec![];
    let selected = knapsack(&items, 10);
    assert!(selected.is_empty());
}

#[test]
fn test_knapsack_exact_fit() {
    let items = vec![
        Item { name: "gold".to_string(), weight: 5, value: 100 },
        Item { name: "silver".to_string(), weight: 5, value: 50 },
    ];
    let selected = knapsack(&items, 5);
    assert_eq!(selected, vec!["gold"]);
}
