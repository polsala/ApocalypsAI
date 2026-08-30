#[cfg(test)]
mod tests {
    use scavenger_knapsack::knapsack;

    #[test]
    fn test_simple_case() {
        // Items: (weight, value)
        let weights = vec![3, 2, 5];
        let values = vec![10, 7, 12];
        let capacity = 7;
        // Best combination: weight 2 + 5 = 7, value 7 + 12 = 19
        assert_eq!(knapsack(&weights, &values, capacity), 19);
    }

    #[test]
    fn test_zero_capacity() {
        let weights = vec![1, 2, 3];
        let values = vec![10, 20, 30];
        assert_eq!(knapsack(&weights, &values, 0), 0);
    }

    #[test]
    fn test_no_items() {
        let weights: Vec<u32> = vec![];
        let values: Vec<u32> = vec![];
        assert_eq!(knapsack(&weights, &values, 10), 0);
    }
}
