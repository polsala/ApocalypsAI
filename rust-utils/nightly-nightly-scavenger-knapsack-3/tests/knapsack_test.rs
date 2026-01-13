#[cfg(test)]
mod tests {
    use crate::knapsack;

    #[test]
    fn test_example() {
        // capacity 15, items (3,4) (4,5) (7,10) (8,11) (9,13)
        let capacity = 15;
        let items = vec![(3,4), (4,5), (7,10), (8,11), (9,13)];
        let result = knapsack(capacity, &items);
        assert_eq!(result, 21); // optimal value is 21 (items 7:10 + 8:11)
    }

    #[test]
    fn test_zero_capacity() {
        let capacity = 0;
        let items = vec![(5,10), (2,3)];
        assert_eq!(knapsack(capacity, &items), 0);
    }

    #[test]
    fn test_no_items() {
        let capacity = 10;
        let items: Vec<(usize, usize)> = vec![];
        assert_eq!(knapsack(capacity, &items), 0);
    }
}

