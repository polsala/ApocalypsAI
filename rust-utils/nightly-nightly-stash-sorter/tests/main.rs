use nightly_stash_sorter::{categorize_item, default_categories, load_custom_rules};
use std::collections::BTreeMap;
use std::fs;

// Mock rationale: We are testing the `load_custom_rules` function which reads a file.
// Creating temporary files allows us to test this function deterministically and offline
// without relying on actual file system state or external resources.
#[test]
fn test_load_custom_rules_success() {
    let test_rules_content = r#"
        [categories.survival_food]
        keywords = ["beans", "ration"]

        [categories.medical_supplies]
        keywords = ["bandages", "medkit"]
    "#;
    let temp_dir = tempfile::tempdir().expect("Failed to create temp dir");
    let file_path = temp_dir.path().join("test_rules.toml");
    fs::write(&file_path, test_rules_content).expect("Failed to write test rules file");

    let rules = load_custom_rules(file_path.to_str().unwrap()).expect("Failed to load custom rules");

    assert_eq!(rules.len(), 2);
    assert!(rules.contains_key("survival_food"));
    assert!(rules.contains_key("medical_supplies"));
    assert_eq!(rules["survival_food"], vec!["beans", "ration"]);
    assert_eq!(rules["medical_supplies"], vec!["bandages", "medkit"]);

    temp_dir.close().expect("Failed to clean up temp dir");
}

// Mock rationale: Similar to the above, testing file reading for error cases.
#[test]
fn test_load_custom_rules_file_not_found() {
    let result = load_custom_rules("non_existent_file.toml");
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Failed to read rules file"));
}

// Mock rationale: Testing file parsing for error cases.
#[test]
fn test_load_custom_rules_invalid_toml() {
    let invalid_toml_content = r#"
        [categories.bad_category
        keywords = ["item"]
    "#;
    let temp_dir = tempfile::tempdir().expect("Failed to create temp dir");
    let file_path = temp_dir.path().join("invalid_rules.toml");
    fs::write(&file_path, invalid_toml_content).expect("Failed to write invalid rules file");

    let result = load_custom_rules(file_path.to_str().unwrap());
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Failed to parse rules file"));

    temp_dir.close().expect("Failed to clean up temp dir");
}

#[test]
fn test_categorize_item_default_rules() {
    let rules = default_categories();

    assert_eq!(categorize_item("can of beans", &rules), "Sustenance");
    assert_eq!(categorize_item("rusty wrench", &rules), "Tools & Tech");
    assert_eq!(categorize_item("shiny button", &rules), "Barter & Bling");
    assert_eq!(categorize_item("glowing orb", &rules), "Mysterious Artifacts");
    assert_eq!(categorize_item("a random rock", &rules), "Miscellaneous");
    assert_eq!(categorize_item("Bottle of Water", &rules), "Sustenance"); // Case insensitive
    assert_eq!(categorize_item("Circuit Board", &rules), "Tools & Tech");
}

#[test]
fn test_categorize_item_with_custom_rules_override() {
    let mut rules = default_categories();
    // Add a custom rule that might override or add to existing ones
    let custom_rules_map: BTreeMap<String, Vec<String>> = [
        ("Sustenance".to_string(), vec!["chocolate".to_string()]), // Add a new keyword to existing category
        ("Rare Finds".to_string(), vec!["diamond".to_string(), "emerald".to_string()]), // New category
    ].iter().cloned().collect();

    for (category_name, keywords) in custom_rules_map {
        rules.entry(category_name).or_default().extend(keywords);
    }

    assert_eq!(categorize_item("chocolate bar", &rules), "Sustenance");
    assert_eq!(categorize_item("raw diamond", &rules), "Rare Finds");
    assert_eq!(categorize_item("can of beans", &rules), "Sustenance"); // Default still works
}

#[test]
fn test_categorize_item_empty_string() {
    let rules = default_categories();
    assert_eq!(categorize_item("", &rules), "Miscellaneous");
}

#[test]
fn test_categorize_item_no_match() {
    let rules = default_categories();
    assert_eq!(categorize_item("a very unique item with no keywords", &rules), "Miscellaneous");
}

// Integration test for the main logic flow (without actual file I/O for input)
// Mock rationale: We cannot directly test `main`'s stdin/stdout without complex mocking.
// Instead, we test the core categorization logic which `main` orchestrates.
// The `main` function's file reading and output formatting are assumed to work
// correctly if the `categorize_item` and `load_custom_rules` functions are correct.
// For a CLI tool, testing the core logic functions is usually sufficient for unit tests.
#[test]
fn test_full_categorization_flow() {
    let mut rules = default_categories();
    let custom_rules_map: BTreeMap<String, Vec<String>> = [
        ("Special Tools".to_string(), vec!["laser".to_string()]),
        ("Rare Finds".to_string(), vec!["gem".to_string()]),
    ].iter().cloned().collect();

    for (category_name, keywords) in custom_rules_map {
        rules.entry(category_name).or_default().extend(keywords);
    }

    let items = vec![
        "old hammer",
        "can of peaches",
        "shiny gem",
        "broken laser pointer",
        "a plain rock",
        "bottle of water",
    ];

    let mut categorized_results: BTreeMap<String, Vec<String>> = BTreeMap::new();
    for category in rules.keys() {
        categorized_results.insert(category.clone(), Vec::new());
    }
    categorized_results.insert("Miscellaneous".to_string(), Vec::new());

    for item in items {
        let category = categorize_item(item, &rules);
        categorized_results.entry(category).or_default().push(item.to_string());
    }

    // Sort items within categories for deterministic comparison
    for (_category, items_list) in categorized_results.iter_mut() {
        items_list.sort();
    }

    assert_eq!(categorized_results["Sustenance"], vec!["bottle of water", "can of peaches"]);
    assert_eq!(categorized_results["Tools & Tech"], vec!["old hammer"]);
    assert_eq!(categorized_results["Barter & Bling"], vec![] as Vec<String>);
    assert_eq!(categorized_results["Mysterious Artifacts"], vec![] as Vec<String>);
    assert_eq!(categorized_results["Special Tools"], vec!["broken laser pointer"]);
    assert_eq!(categorized_results["Rare Finds"], vec!["shiny gem"]);
    assert_eq!(categorized_results["Miscellaneous"], vec!["a plain rock"]);
}
