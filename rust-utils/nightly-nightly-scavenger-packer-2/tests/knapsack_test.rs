use nightly_scavenger_packer::lib::{Item, solve_knapsack};

#[test]
fn test_knapsack_basic() {
    let items = vec![
        Item { name: "A".into(), weight: 3, value: 4 },
        Item { name: "B".into(), weight: 4, value: 5 },
        Item { name: "C".into(), weight: 2, value: 3 },
    ];
    let capacity = 6;
    let selected = solve_knapsack(&items, capacity);
    // Optimal selection is items B and C (weight 6, value 8)
    assert_eq!(selected.len(), 2);
    let names: Vec<_> = selected.iter().map(|i| i.name.as_str()).collect();
    assert!(names.contains(&"B"));
    assert!(names.contains(&"C"));
    let total_value: u32 = selected.iter().map(|i| i.value).sum();
    assert_eq!(total_value, 8);
}
