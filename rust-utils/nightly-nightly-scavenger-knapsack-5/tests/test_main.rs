#[cfg(test)]
mod tests {
    use super::super::lib::{Item, knapsack};

    #[test]
    fn test_knapsack_all_items_fit() {
        let items = vec![
            Item { name: "apple".to_string(), weight: 2, value: 5 },
            Item { name: "water".to_string(), weight: 3, value: 8 },
            Item { name: "medkit".to_string(), weight: 5, value: 12 },
        ];
        let (selected, total) = knapsack(&items, 10);
        assert_eq!(selected, vec!["apple", "water", "medkit"]);
        assert_eq!(total, 25);
    }

    #[test]
    fn test_knapsack_capacity_too_small() {
        let items = vec![
            Item { name: "rock".to_string(), weight: 5, value: 1 },
            Item { name: "gold".to_string(), weight: 4, value: 10 },
        ];
        let (selected, total) = knapsack(&items, 3);
        assert!(selected.is_empty());
        assert_eq!(total, 0);
    }
}
