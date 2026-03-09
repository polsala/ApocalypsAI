#[cfg(test)]
mod tests {
    use super::super::*;
    use scavenger_optimize::{parse_items, optimal_subset, Item};

    #[test]
    fn test_parse_items() {
        let s = "2:5:water,1:3:food,3:9:medicine";
        let items = parse_items(s);
        assert_eq!(items.len(), 3);
        assert_eq!(items[0].weight, 2);
        assert_eq!(items[0].value, 5);
        assert_eq!(items[0].name, "water");
    }

    #[test]
    fn test_optimal_subset_basic() {
        let items = vec![
            Item { name: "water".to_string(), weight: 2, value: 5 },
            Item { name: "food".to_string(), weight: 1, value: 3 },
            Item { name: "medicine".to_string(), weight: 3, value: 9 },
        ];
        let result = optimal_subset(5, &items);
        // Best combination is water + medicine (weight 5, value 14)
        assert_eq!(result.len(), 2);
        let names: Vec<&str> = result.iter().map(|i| i.name.as_str()).collect();
        assert!(names.contains(&"water"));
        assert!(names.contains(&"medicine"));
    }

    #[test]
    fn test_optimal_subset_no_fit() {
        let items = vec![
            Item { name: "rock".to_string(), weight: 10, value: 1 },
        ];
        let result = optimal_subset(5, &items);
        assert!(result.is_empty());
    }
}
