use super::{parse_manifest, Category};
use std::collections::HashMap;

#[test]
fn test_empty_manifest() {
    // Mock rationale: Providing hardcoded string input for deterministic testing.
    let input = "";
    let result = parse_manifest(input);
    assert!(result.is_empty());
}

#[test]
fn test_simple_items() {
    // Mock rationale: Providing hardcoded string input for deterministic testing.
    let input = "3x Canned Beans\nRusty Wrench\nWater Bottle\n5x Scrap Metal";
    let result = parse_manifest(input);

    assert_eq!(result.len(), 4); // Food, Tools, Water, Components

    let food_items = result.get(&Category::Food).unwrap();
    assert_eq!(food_items.get("Canned Beans"), Some(&3));

    let tool_items = result.get(&Category::Tools).unwrap();
    assert_eq!(tool_items.get("Rusty Wrench"), Some(&1));

    let water_items = result.get(&Category::Water).unwrap();
    assert_eq!(water_items.get("Water Bottle"), Some(&1));

    let component_items = result.get(&Category::Components).unwrap();
    assert_eq!(component_items.get("Scrap Metal"), Some(&5));
}

#[test]
fn test_mixed_quantities_and_duplicates() {
    // Mock rationale: Providing hardcoded string input for deterministic testing.
    let input = "2x Canned Beans\nCanned Beans\n10x Scrap Metal\n3x Wire\nScrap Metal";
    let result = parse_manifest(input);

    let food_items = result.get(&Category::Food).unwrap();
    assert_eq!(food_items.get("Canned Beans"), Some(&3)); // 2 + 1

    let component_items = result.get(&Category::Components).unwrap();
    assert_eq!(component_items.get("Scrap Metal"), Some(&11)); // 10 + 1
    assert_eq!(component_items.get("Wire"), Some(&3));
}

#[test]
fn test_unknown_items() {
    // Mock rationale: Providing hardcoded string input for deterministic testing.
    let input = "Mysterious Orb\nShiny Rock\nBroken Gadget";
    let result = parse_manifest(input);

    let unknown_items = result.get(&Category::Unknown).unwrap();
    assert_eq!(unknown_items.get("Mysterious Orb"), Some(&1));

    let junk_items = result.get(&Category::Junk).unwrap();
    assert_eq!(junk_items.get("Shiny Rock"), Some(&1)); // "rock" keyword
    assert_eq!(junk_items.get("Broken Gadget"), Some(&1)); // "broken" keyword
}

#[test]
fn test_category_classification() {
    assert_eq!(Category::classify("Fresh Berries"), Category::Food);
    assert_eq!(Category::classify("Purified Water"), Category::Water);
    assert_eq!(Category::classify("Multi-tool"), Category::Tools);
    assert_eq!(Category::classify("Copper Wire"), Category::Components);
    assert_eq!(Category::classify("First Aid Kit"), Category::Medical);
    assert_eq!(Category::classify("Pile of Dirt"), Category::Junk);
    assert_eq!(Category::classify("Ancient Scroll"), Category::Unknown);
    assert_eq!(Category::classify("Rusty Nail"), Category::Junk);
    assert_eq!(Category::classify("Old Boot"), Category::Junk);
    assert_eq!(Category::classify("Dried Fruit"), Category::Food);
}

#[test]
fn test_whitespace_handling() {
    // Mock rationale: Providing hardcoded string input for deterministic testing.
    let input = "  5x   Old Bolts  \n\n  Rusty Knife   ";
    let result = parse_manifest(input);

    let component_items = result.get(&Category::Components).unwrap();
    assert_eq!(component_items.get("Old Bolts"), Some(&5));

    let tool_items = result.get(&Category::Tools).unwrap();
    assert_eq!(tool_items.get("Rusty Knife"), Some(&1));
}

#[test]
fn test_no_quantity_items() {
    // Mock rationale: Providing hardcoded string input for deterministic testing.
    let input = "Canned Soup\nHammer\nWater";
    let result = parse_manifest(input);

    let food_items = result.get(&Category::Food).unwrap();
    assert_eq!(food_items.get("Canned Soup"), Some(&1));

    let tool_items = result.get(&Category::Tools).unwrap();
    assert_eq!(tool_items.get("Hammer"), Some(&1));

    let water_items = result.get(&Category::Water).unwrap();
    assert_eq!(water_items.get("Water"), Some(&1));
}
