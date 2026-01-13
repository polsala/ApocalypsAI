#[cfg(test)]
mod tests {
    use nightly_survival_gear_optimizer::lib::{Item, solve_knapsack};

    #[test]
    fn test_simple_case() {
        let items = vec![
            Item { name: "Water".to_string(), weight: 3, utility: 10 },
            Item { name: "Food".to_string(), weight: 4, utility: 12 },
            Item { name: "Radio".to_string(), weight: 2, utility: 7 },
        ];
        let selected = solve_knapsack(&items, 5);
        // Best utility: Water (3,10) + Radio (2,7) = 17
        assert_eq!(selected, vec!["Water".to_string(), "Radio".to_string()]);
    }

    #[test]
    fn test_no_items() {
        let items: Vec<Item> = vec![];
        let selected = solve_knapsack(&items, 10);
        assert!(selected.is_empty());
    }

    #[test]
    fn test_exact_fit() {
        let items = vec![
            Item { name: "A".to_string(), weight: 5, utility: 8 },
            Item { name: "B".to_string(), weight: 3, utility: 5 },
            Item { name: "C".to_string(), weight: 2, utility: 3 },
        ];
        let selected = solve_knapsack(&items, 10);
        // All items fit within capacity 10
        assert_eq!(selected.len(), 3);
        assert!(selected.contains(&"A".to_string()));
        assert!(selected.contains(&"B".to_string()));
        assert!(selected.contains(&"C".to_string()));
    }
}

