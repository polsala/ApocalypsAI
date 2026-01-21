use scavenger_knapsack::{compute_knapsack, Item, Payload};

#[test]
fn test_simple_knapsack() {
    let payload = Payload {
        capacity: 10,
        items: vec![
            Item { name: "canned beans".to_string(), weight: 3, value: 5 },
            Item { name: "water bottle".to_string(), weight: 2, value: 4 },
            Item { name: "first aid kit".to_string(), weight: 5, value: 10 },
        ],
    };
    let result = compute_knapsack(&payload);
    // Expected optimal selection: canned beans + first aid kit (weight 8, value 15)
    let expected = vec!["canned beans".to_string(), "first aid kit".to_string()];
    assert_eq!(result, expected);
}
