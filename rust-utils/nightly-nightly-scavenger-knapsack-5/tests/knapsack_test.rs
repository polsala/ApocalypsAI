#[cfg(test)]
mod tests {
    use super::super::lib::{compute_knapsack, Item, Problem};

    #[test]
    fn test_basic_scenario() {
        // Mock rationale: simple deterministic dataset to verify optimal selection
        let problem = Problem {
            capacity: 10,
            items: vec![
                Item { name: "canned-food".into(), weight: 3, value: 5 },
                Item { name: "water-bottle".into(), weight: 4, value: 4 },
                Item { name: "first-aid-kit".into(), weight: 5, value: 7 },
                Item { name: "radio".into(), weight: 2, value: 3 },
            ],
        };
        let result = compute_knapsack(&problem);
        // Expected optimal set: canned-food (3,5) + first-aid-kit (5,7) = weight 8, value 12
        // radio (2,3) could also be added but would exceed capacity (10) if combined with both above.
        let expected = vec!["canned-food", "first-aid-kit"];
        assert_eq!(result, expected);
    }

    #[test]
    fn test_exact_fit() {
        // Mock rationale: ensure algorithm picks items that exactly fill capacity when possible
        let problem = Problem {
            capacity: 7,
            items: vec![
                Item { name: "knife".into(), weight: 2, value: 3 },
                Item { name: "torch".into(), weight: 3, value: 4 },
                Item { name: "map".into(), weight: 5, value: 6 },
            ],
        };
        let result = compute_knapsack(&problem);
        // Best value is knife + torch = weight 5, value 7 (better than map alone)
        let expected = vec!["knife", "torch"];
        assert_eq!(result, expected);
    }
}
