#[cfg(test)]
mod tests {
    use super::*;
    use crate::lib::{Item, solve_knapsack};

    #[test]
    fn test_basic_knapsack() {
        // Mock rationale: simple deterministic scenario to verify optimal selection.
        let limit = 10usize;
        let items = vec![
            Item { name: "water".to_string(), weight: 5, value: 10 },
            Item { name: "food".to_string(), weight: 4, value: 7 },
            Item { name: "medkit".to_string(), weight: 6, value: 12 },
        ];
        let result = solve_knapsack(limit, &items);
        assert_eq!(result, vec!["water".to_string(), "food".to_string()]);
    }

    #[test]
    fn test_exact_fit() {
        // Mock rationale: ensure algorithm picks exact‑fit when values are equal.
        let limit = 8usize;
        let items = vec![
            Item { name: "radio".to_string(), weight: 3, value: 5 },
            Item { name: "map".to_string(), weight: 5, value: 5 },
            Item { name: "torch".to_string(), weight: 4, value: 4 },
        ];
        let result = solve_knapsack(limit, &items);
        // Best total value is 10 (radio+map) which fits exactly 8 weight.
        assert_eq!(result, vec!["radio".to_string(), "map".to_string()]);
    }
}
