use knapsack_scrap_optimizer::{Item, knapsack};

#[test]
fn test_knapsack_basic() {
    let items = vec![
        Item { name: "A".to_string(), weight: 3, value: 4 },
        Item { name: "B".to_string(), weight: 4, value: 5 },
        Item { name: "C".to_string(), weight: 2, value: 3 },
    ];
    // With max weight 6, optimal selection is items B and C (value 8)
    let (value, indices) = knapsack(&items, 6);
    assert_eq!(value, 8);
    assert_eq!(indices, vec![1, 2]); // indices of B and C
}
