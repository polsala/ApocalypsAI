use scavenger_packer::lib::{Item, knapsack};

#[test]
fn test_integration_knapsack() {
    // Mock rationale: deterministic small dataset for verification
    let items = vec![
        Item { name: "mutated radroach".into(), weight: 3, value: 10 },
        Item { name: "scrap metal".into(), weight: 5, value: 7 },
        Item { name: "bottled water".into(), weight: 2, value: 5 },
        Item { name: "old battery".into(), weight: 4, value: 8 },
    ];
    let capacity = 7;
    let selected = knapsack(&items, capacity);
    // Expected optimal selection: mutated radroach + bottled water (weight 5, value 15)
    assert_eq!(selected.len(), 2);
    assert!(selected.iter().any(|i| i.name == "mutated radroach"));
    assert!(selected.iter().any(|i| i.name == "bottled water"));
    let total_weight: u32 = selected.iter().map(|i| i.weight).sum();
    let total_value: u32 = selected.iter().map(|i| i.value).sum();
    assert_eq!(total_weight, 5);
    assert_eq!(total_value, 15);
}
