#[cfg(test)]
mod tests {
    use scavenger_knapsack::lib::{Item, solve_knapsack};

    #[test]
    fn test_simple_case() {
        let items = vec![
            Item { name: "A".to_string(), weight: 3, value: 4 },
            Item { name: "B".to_string(), weight: 4, value: 5 },
            Item { name: "C".to_string(), weight: 2, value: 3 },
        ];
        let result = solve_knapsack(&items, 6);
        let names: Vec<&str> = result.iter().map(|i| i.name.as_str()).collect();
        // Optimal selection is items B and C (total weight 6, total value 8)
        assert_eq!(names, vec!["B", "C"]);
    }

    #[test]
    fn test_zero_capacity() {
        let items = vec![
            Item { name: "X".to_string(), weight: 1, value: 10 },
        ];
        let result = solve_knapsack(&items, 0);
        assert!(result.is_empty());
    }
}
