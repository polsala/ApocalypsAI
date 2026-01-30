use scavenger_knapsack::{knapsack, Item};

#[test]
fn test_knapsack_basic() {
    let items = vec![
        Item { name: "water".to_string(), weight: 3, utility: 10 },
        Item { name: "food".to_string(), weight: 2, utility: 8 },
        Item { name: "radio".to_string(), weight: 1, utility: 5 },
    ];
    let selected = knapsack(&items, 5);
    let selected_names: Vec<&str> = selected.iter().map(|&i| items[i].name.as_str()).collect();
    // Optimal selection is water (3,10) + food (2,8) = utility 18
    assert_eq!(selected_names, vec!["water", "food"]);
}
