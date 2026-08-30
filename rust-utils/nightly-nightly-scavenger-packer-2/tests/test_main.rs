use scavenger_packer::{Item, knapsack};

#[test]
fn test_knapsack_example() {
    let items = vec![
        Item { name: "canned".into(), weight: 3, value: 10 },
        Item { name: "water".into(), weight: 5, value: 8 },
        Item { name: "medkit".into(), weight: 4, value: 12 },
    ];
    // Capacity 7 allows picking medkit (4) + canned (3) for total value 22.
    let (max, selected) = knapsack(&items, 7);
    assert_eq!(max, 22);
    assert_eq!(selected, vec![0, 2]); // indices of canned and medkit
}
