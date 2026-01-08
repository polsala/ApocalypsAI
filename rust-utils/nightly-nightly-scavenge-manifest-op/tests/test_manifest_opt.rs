use super::{Item, optimize_manifest}; // Assuming `super` works for integration tests

#[test]
fn test_optimize_manifest_empty_items() {
    // Mock rationale: This test directly invokes the `optimize_manifest` function
    // with an empty `Item` vector, simulating an empty manifest without
    // requiring actual file I/O. This ensures determinism and offline execution.
    let items = vec![];
    let weight_limit = 10;
    let (value, weight, chosen) = optimize_manifest(&items, weight_limit);
    assert_eq!(value, 0);
    assert_eq!(weight, 0);
    assert!(chosen.is_empty());
}

#[test]
fn test_optimize_manifest_single_item_fits() {
    // Mock rationale: This test directly invokes the `optimize_manifest` function
    // with predefined `Item` vectors, simulating various input scenarios without
    // requiring actual file I/O. This ensures determinism and offline execution.
    let items = vec![
        Item { name: "Water Bottle".to_string(), weight: 2, value: 5 },
    ];
    let weight_limit = 3;
    let (value, weight, chosen) = optimize_manifest(&items, weight_limit);
    assert_eq!(value, 5);
    assert_eq!(weight, 2);
    assert_eq!(chosen.len(), 1);
    assert_eq!(chosen[0].name, "Water Bottle");
}

#[test]
fn test_optimize_manifest_single_item_too_heavy() {
    // Mock rationale: See above.
    let items = vec![
        Item { name: "Heavy Armor".to_string(), weight: 15, value: 100 },
    ];
    let weight_limit = 10;
    let (value, weight, chosen) = optimize_manifest(&items, weight_limit);
    assert_eq!(value, 0);
    assert_eq!(weight, 0);
    assert!(chosen.is_empty());
}

#[test]
fn test_optimize_manifest_multiple_items_all_fit() {
    // Mock rationale: See above.
    let items = vec![
        Item { name: "Rope".to_string(), weight: 3, value: 10 },
        Item { name: "Medkit".to_string(), weight: 2, value: 15 },
    ];
    let weight_limit = 6;
    let (value, weight, chosen) = optimize_manifest(&items, weight_limit);
    assert_eq!(value, 25);
    assert_eq!(weight, 5);
    assert_eq!(chosen.len(), 2);
    // Order might vary depending on reconstruction, check for presence
    assert!(chosen.iter().any(|i| i.name == "Rope"));
    assert!(chosen.iter().any(|i| i.name == "Medkit"));
}

#[test]
fn test_optimize_manifest_knapsack_classic() {
    // Mock rationale: See above.
    // Items: (weight, value)
    // A: (10, 60)
    // B: (20, 100)
    // C: (30, 120)
    // Weight limit: 50
    // Optimal: B + C = (20+30=50 weight, 100+120=220 value)
    let items = vec![
        Item { name: "Item A".to_string(), weight: 10, value: 60 },
        Item { name: "Item B".to_string(), weight: 20, value: 100 },
        Item { name: "Item C".to_string(), weight: 30, value: 120 },
    ];
    let weight_limit = 50;
    let (value, weight, chosen) = optimize_manifest(&items, weight_limit);
    assert_eq!(value, 220);
    assert_eq!(weight, 50);
    assert_eq!(chosen.len(), 2);
    assert!(chosen.iter().any(|i| i.name == "Item B"));
    assert!(chosen.iter().any(|i| i.name == "Item C"));
}

#[test]
fn test_optimize_manifest_partial_fit() {
    // Mock rationale: See above.
    let items = vec![
        Item { name: "Small Battery".to_string(), weight: 1, value: 10 },
        Item { name: "Large Battery".to_string(), weight: 5, value: 40 },
        Item { name: "Scrap Metal".to_string(), weight: 3, value: 15 },
    ];
    let weight_limit = 7;
    // Options:
    // SB (1,10) + LB (5,40) = (6, 50)
    // SB (1,10) + SM (3,15) = (4, 25)
    // LB (5,40) + SM (3,15) = (8, 55) -> too heavy
    // Optimal: Small Battery + Large Battery
    let (value, weight, chosen) = optimize_manifest(&items, weight_limit);
    assert_eq!(value, 50);
    assert_eq!(weight, 6);
    assert_eq!(chosen.len(), 2);
    assert!(chosen.iter().any(|i| i.name == "Small Battery"));
    assert!(chosen.iter().any(|i| i.name == "Large Battery"));
}

#[test]
fn test_optimize_manifest_zero_limit() {
    // Mock rationale: See above.
    let items = vec![
        Item { name: "Item A".to_string(), weight: 1, value: 10 },
    ];
    let weight_limit = 0;
    let (value, weight, chosen) = optimize_manifest(&items, weight_limit);
    assert_eq!(value, 0);
    assert_eq!(weight, 0);
    assert!(chosen.is_empty());
}

#[test]
fn test_optimize_manifest_items_with_zero_weight() {
    // Mock rationale: See above.
    let items = vec![
        Item { name: "Heavy Item".to_string(), weight: 10, value: 50 },
        Item { name: "Light Item".to_string(), weight: 1, value: 5 },
        Item { name: "Zero Weight Item".to_string(), weight: 0, value: 100 },
    ];
    let weight_limit = 10;
    // Optimal: Zero Weight Item (0, 100) + Heavy Item (10, 50) = (10, 150)
    let (value, weight, chosen) = optimize_manifest(&items, weight_limit);
    assert_eq!(value, 150);
    assert_eq!(weight, 10);
    assert_eq!(chosen.len(), 2);
    assert!(chosen.iter().any(|i| i.name == "Heavy Item"));
    assert!(chosen.iter().any(|i| i.name == "Zero Weight Item"));
}

#[test]
fn test_optimize_manifest_duplicate_items() {
    // Mock rationale: See above.
    let items = vec![
        Item { name: "Ration Pack".to_string(), weight: 2, value: 10 },
        Item { name: "Ration Pack".to_string(), weight: 2, value: 10 },
        Item { name: "Water Pouch".to_string(), weight: 3, value: 15 },
    ];
    let weight_limit = 5;
    // Optimal: One Ration Pack + Water Pouch = (2+3=5 weight, 10+15=25 value)
    // Or two Ration Packs = (2+2=4 weight, 10+10=20 value)
    let (value, weight, chosen) = optimize_manifest(&items, weight_limit);
    assert_eq!(value, 25);
    assert_eq!(weight, 5);
    assert_eq!(chosen.len(), 2);
    assert!(chosen.iter().any(|i| i.name == "Ration Pack"));
    assert!(chosen.iter().any(|i| i.name == "Water Pouch"));
}
