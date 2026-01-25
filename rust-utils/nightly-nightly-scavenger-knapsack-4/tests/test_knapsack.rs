use nightly_scavenger_knapsack::lib::{Item, knapsack};

#[test]
fn integration_knapsack() {
    let items = vec![
        Item { name: "water".into(), weight: 3, value: 10 },
        Item { name: "food".into(), weight: 2, value: 9 },
        Item { name: "radio".into(), weight: 1, value: 4 },
    ];
    let result = knapsack(&items, 5);
    assert_eq!(result, vec!["food".to_string(), "radio".to_string()]);
}
