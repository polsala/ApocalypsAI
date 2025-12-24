use serde::{Deserialize, Serialize};
use std::fs;
use std::path::Path;

#[derive(Debug, Serialize, Deserialize, Clone, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub quantity: u32,
    /// Days until the item expires (0 = already expired)
    pub expires_in_days: u32,
}

/// Load inventory from a JSON file. If the file does not exist, returns an empty vec.
pub fn load_inventory<P: AsRef<Path>>(path: P) -> Result<Vec<Item>, String> {
    if !path.as_ref().exists() {
        return Ok(Vec::new());
    }
    let data = fs::read_to_string(&path).map_err(|e| format!("Failed to read {}: {}", path.as_ref().display(), e))?;
    serde_json::from_str(&data).map_err(|e| format!("Failed to parse JSON: {}", e))
}

/// Save inventory to a JSON file.
pub fn save_inventory<P: AsRef<Path>>(path: P, items: &[Item]) -> Result<(), String> {
    let json = serde_json::to_string_pretty(items).map_err(|e| format!("Serialization error: {}", e))?;
    fs::write(&path, json).map_err(|e| format!("Failed to write {}: {}", path.as_ref().display(), e))
}

/// Add a new item to the inventory, merging with existing entry of same name.
pub fn add_item(mut items: Vec<Item>, new_item: Item) -> Vec<Item> {
    for item in items.iter_mut() {
        if item.name.eq_ignore_ascii_case(&new_item.name) {
            item.quantity += new_item.quantity;
            // Keep the smallest expiration (most urgent)
            if new_item.expires_in_days < item.expires_in_days {
                item.expires_in_days = new_item.expires_in_days;
            }
            return items;
        }
    }
    items.push(new_item);
    items
}

/// Return items sorted by `expires_in_days` ascending.
pub fn sorted_by_expiration(mut items: Vec<Item>) -> Vec<Item> {
    items.sort_by_key(|i| i.expires_in_days);
    items
}

/// Suggest the next item to consume (the one expiring soonest). Returns None if inventory empty.
pub fn suggest_next(items: &[Item]) -> Option<Item> {
    items.iter().min_by_key(|i| i.expires_in_days).cloned()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_and_merge() {
        let existing = vec![Item { name: "Canned Beans".into(), quantity: 2, expires_in_days: 300 }];
        let new = Item { name: "canned beans".into(), quantity: 3, expires_in_days: 250 };
        let result = add_item(existing, new);
        assert_eq!(result.len(), 1);
        assert_eq!(result[0].quantity, 5);
        assert_eq!(result[0].expires_in_days, 250);
    }

    #[test]
    fn test_sorting() {
        let mut items = vec![
            Item { name: "Water".into(), quantity: 10, expires_in_days: 500 },
            Item { name: "Bread".into(), quantity: 2, expires_in_days: 2 },
            Item { name: "Jerky".into(), quantity: 5, expires_in_days: 180 },
        ];
        let sorted = sorted_by_expiration(items.clone());
        assert_eq!(sorted[0].name, "Bread");
        assert_eq!(sorted[1].name, "Jerky");
        assert_eq!(sorted[2].name, "Water");
    }

    #[test]
    fn test_suggest_next() {
        let items = vec![
            Item { name: "Water".into(), quantity: 10, expires_in_days: 500 },
            Item { name: "Bread".into(), quantity: 2, expires_in_days: 2 },
        ];
        let suggestion = suggest_next(&items).unwrap();
        assert_eq!(suggestion.name, "Bread");
    }
}
