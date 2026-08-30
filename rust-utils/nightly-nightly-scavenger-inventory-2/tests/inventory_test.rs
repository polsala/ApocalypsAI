#[cfg(test)]
mod tests {
    use super::super::lib::{add_item, deserialize_inventory, serialize_inventory, prioritize, Item};

    #[test]
    fn test_add_and_serialize() {
        let inventory = Vec::new();
        let item = Item {
            name: "Canned Beans".to_string(),
            category: "food".to_string(),
            quantity: 12,
            expires_in_days: 180,
        };
        let inventory = add_item(inventory, item.clone());
        let json = serialize_inventory(&inventory);
        let deserialized = deserialize_inventory(&json);
        assert_eq!(deserialized, vec![item]);
    }

    #[test]
    fn test_prioritize() {
        let items = vec![
            Item { name: "Water Bottle".to_string(), category: "drink".to_string(), quantity: 5, expires_in_days: 365 },
            Item { name: "Fresh Fruit".to_string(), category: "food".to_string(), quantity: 3, expires_in_days: 5 },
            Item { name: "Bandage".to_string(), category: "medical".to_string(), quantity: 20, expires_in_days: 730 },
        ];
        let urgent = prioritize(&items).expect("Should have at least one item");
        assert_eq!(urgent.name, "Fresh Fruit");
        assert_eq!(urgent.expires_in_days, 5);
    }
}
