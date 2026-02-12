use nightly_scavenger_knapsack::{Item, greedy_knapsack};

#[test]
fn test_greedy_knapsack_basic() {
    let items = vec![
        Item { name: "A".to_string(), weight: 2, value: 6 },
        Item { name: "B".to_string(), weight: 3, value: 5 },
        Item { name: "C".to_string(), weight: 5, value: 10 },
        Item { name: "D".to_string(), weight: 1, value: 2 },
    ];
    let result = greedy_knapsack(&items, 7);
    let names: Vec<&str> = result.iter().map(|i| i.name.as_str()).collect();
    // Greedy picks A (ratio 3.0) then C (ratio 2.0); total weight 7, total value 16
    assert_eq!(names, vec!["A", "C"]);
    let total_value: u32 = result.iter().map(|i| i.value).sum();
    assert_eq!(total_value, 16);
}
