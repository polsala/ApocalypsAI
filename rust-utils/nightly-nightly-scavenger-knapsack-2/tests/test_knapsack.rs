use scavenger_knapsack::lib::{Item, solve_knapsack};

#[test]
fn test_basic() {
    let items = vec![
        Item { name: "Water".to_string(), weight: 3, value: 10 },
        Item { name: "Food".to_string(), weight: 2, value: 7 },
        Item { name: "Medkit".to_string(), weight: 5, value: 12 },
    ];
    let result = solve_knapsack(&items, 5);
    // Best combination: Water (3,10) + Food (2,7) = value 17
    assert_eq!(result.len(), 2);
    assert!(result.iter().any(|i| i.name == "Water"));
    assert!(result.iter().any(|i| i.name == "Food"));
}

#[test]
fn test_zero_capacity() {
    let items = vec![
        Item { name: "A".to_string(), weight: 1, value: 1 },
    ];
    let result = solve_knapsack(&items, 0);
    assert!(result.is_empty());
}

#[test]
fn test_all_fit() {
    let items = vec![
        Item { name: "A".to_string(), weight: 1, value: 1 },
        Item { name: "B".to_string(), weight: 2, value: 2 },
    ];
    let result = solve_knapsack(&items, 10);
    assert_eq!(result.len(), 2);
    assert!(result.iter().any(|i| i.name == "A"));
    assert!(result.iter().any(|i| i.name == "B"));
}
