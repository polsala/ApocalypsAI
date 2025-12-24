use std::fs;
use std::path::PathBuf;

use nightly_scavenger_inventory::lib::{add_item, load_inventory, save_inventory, suggest_next, sorted_by_expiration, Item};

#[test]
fn test_load_save_cycle() {
    // Mock inventory file path in a temporary directory
    let tmp_dir = tempfile::tempdir().expect("tempdir");
    let inv_path = tmp_dir.path().join("inv.json");

    let items = vec![
        Item { name: "Canned Tuna".into(), quantity: 3, expires_in_days: 400 },
        Item { name: "Bread".into(), quantity: 1, expires_in_days: 2 },
    ];
    // Save
    save_inventory(&inv_path, &items).expect("save");
    // Load
    let loaded = load_inventory(&inv_path).expect("load");
    assert_eq!(items, loaded);
}

#[test]
fn test_suggest_and_sort() {
    let items = vec![
        Item { name: "Water".into(), quantity: 5, expires_in_days: 365 },
        Item { name: "Bread".into(), quantity: 2, expires_in_days: 1 },
        Item { name: "Jerky".into(), quantity: 10, expires_in_days: 180 },
    ];
    let suggestion = suggest_next(&items).unwrap();
    assert_eq!(suggestion.name, "Bread");

    let sorted = sorted_by_expiration(items.clone());
    assert_eq!(sorted[0].name, "Bread");
    assert_eq!(sorted[1].name, "Jerky");
    assert_eq!(sorted[2].name, "Water");
}

#[test]
fn test_add_merges_correctly() {
    let existing = vec![Item { name: "Canned Beans".into(), quantity: 2, expires_in_days: 300 }];
    let new = Item { name: "canned beans".into(), quantity: 3, expires_in_days: 250 };
    let result = add_item(existing, new);
    assert_eq!(result.len(), 1);
    assert_eq!(result[0].quantity, 5);
    assert_eq!(result[0].expires_in_days, 250);
}
