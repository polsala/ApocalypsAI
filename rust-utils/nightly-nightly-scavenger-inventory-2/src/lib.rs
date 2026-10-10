use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct Item {
    pub name: String,
    pub category: String,
    pub quantity: u32,
    pub expires_in_days: u32,
}

/// Add an item to the inventory vector.
pub fn add_item(mut inventory: Vec<Item>, item: Item) -> Vec<Item> {
    inventory.push(item);
    inventory
}

/// Return a reference‑sorted slice of items by expiration (soonest first).
pub fn prioritize(inventory: &[Item]) -> Option<&Item> {
    inventory.iter().min_by_key(|i| i.expires_in_days)
}

/// Serialize the inventory to a JSON string.
pub fn serialize_inventory(inventory: &[Item]) -> String {
    serde_json::to_string_pretty(inventory).unwrap()
}

/// Deserialize a JSON string into an inventory vector.
pub fn deserialize_inventory(json: &str) -> Vec<Item> {
    serde_json::from_str(json).unwrap_or_default()
}
