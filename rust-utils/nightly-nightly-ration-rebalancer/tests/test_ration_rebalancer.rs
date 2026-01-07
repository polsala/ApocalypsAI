use super::{
    calculate_ration_plan, load_ration_items, save_remaining_items, RationItem, RationPlan,
};
use std::error::Error;
use std::fs;
use std::path::PathBuf;

// Mock rationale: These tests create temporary files to simulate file I/O.
// This ensures tests are deterministic, offline, and self-contained without relying on external file system state.

#[test]
fn test_load_ration_items() -> Result<(), Box<dyn Error>> {
    let csv_content = "name,calories_per_unit,units_available,perishability_score\nCanned Beans,200,10,1\nFresh Apple,95,3,5\n";
    let temp_dir = tempfile::tempdir()?;
    let file_path = temp_dir.path().join("test_inventory.csv");
    fs::write(&file_path, csv_content)?;

    let items = load_ration_items(&file_path)?;

    assert_eq!(items.len(), 2);
    assert_eq!(items[0].name, "Canned Beans");
    assert_eq!(items[0].calories_per_unit, 200);
    assert_eq!(items[0].units_available, 10);
    assert_eq!(items[0].perishability_score, 1);
    assert_eq!(items[1].name, "Fresh Apple");
    assert_eq!(items[1].calories_per_unit, 95);
    assert_eq!(items[1].units_available, 3);
    assert_eq!(items[1].perishability_score, 5);

    Ok(())
}

#[test]
fn test_calculate_ration_plan_basic() {
    let mut items = vec![
        RationItem {
            name: "Canned Beans".to_string(),
            calories_per_unit: 200,
            units_available: 10,
            perishability_score: 1,
        },
        RationItem {
            name: "Fresh Apple".to_string(),
            calories_per_unit: 95,
            units_available: 3,
            perishability_score: 5,
        },
        RationItem {
            name: "MRE".to_string(),
            calories_per_unit: 1200,
            units_available: 1,
            perishability_score: 1,
        },
    ];
    let target = 1500;

    let (plan, remaining_items) = calculate_ration_plan(&mut items, target);

    assert_eq!(plan.total_consumed_calories, 1485); // 3 apples (285) + 1 MRE (1200)
    assert_eq!(plan.consumed_items.len(), 2);
    assert_eq!(plan.consumed_items[0].0, "Fresh Apple");
    assert_eq!(plan.consumed_items[0].1, 3);
    assert_eq!(plan.consumed_items[1].0, "MRE");
    assert_eq!(plan.consumed_items[1].1, 1);

    // Check remaining items
    assert_eq!(remaining_items[0].name, "Fresh Apple"); // Perishability 5
    assert_eq!(remaining_items[0].units_available, 0);
    assert_eq!(remaining_items[1].name, "MRE"); // Perishability 1
    assert_eq!(remaining_items[1].units_available, 0);
    assert_eq!(remaining_items[2].name, "Canned Beans"); // Perishability 1
    assert_eq!(remaining_items[2].units_available, 10);
}

#[test]
fn test_calculate_ration_plan_exceed_target() {
    let mut items = vec![
        RationItem {
            name: "Survival Bar".to_string(),
            calories_per_unit: 300,
            units_available: 5,
            perishability_score: 2,
        },
    ];
    let target = 200;

    let (plan, remaining_items) = calculate_ration_plan(&mut items, target);

    assert_eq!(plan.total_consumed_calories, 300); // Consumes 1 bar, goes over target
    assert_eq!(plan.consumed_items.len(), 1);
    assert_eq!(plan.consumed_items[0].0, "Survival Bar");
    assert_eq!(plan.consumed_items[0].1, 1);

    assert_eq!(remaining_items[0].units_available, 4);
}

#[test]
fn test_calculate_ration_plan_no_items() {
    let mut items = vec![];
    let target = 1000;

    let (plan, remaining_items) = calculate_ration_plan(&mut items, target);

    assert_eq!(plan.total_consumed_calories, 0);
    assert!(plan.consumed_items.is_empty());
    assert!(remaining_items.is_empty());
}

#[test]
fn test_calculate_ration_plan_not_enough_calories() {
    let mut items = vec![
        RationItem {
            name: "Small Berry".to_string(),
            calories_per_unit: 10,
            units_available: 5,
            perishability_score: 4,
        },
    ];
    let target = 100;

    let (plan, remaining_items) = calculate_ration_plan(&mut items, target);

    assert_eq!(plan.total_consumed_calories, 50);
    assert_eq!(plan.consumed_items.len(), 1);
    assert_eq!(plan.consumed_items[0].0, "Small Berry");
    assert_eq!(plan.consumed_items[0].1, 5);

    assert_eq!(remaining_items[0].units_available, 0);
}

#[test]
fn test_save_remaining_items() -> Result<(), Box<dyn Error>> {
    let items = vec![
        RationItem {
            name: "Canned Soup".to_string(),
            calories_per_unit: 150,
            units_available: 5,
            perishability_score: 1,
        },
    ];
    let temp_dir = tempfile::tempdir()?;
    let output_path = temp_dir.path().join("output_inventory.csv");

    save_remaining_items(&output_path, &items)?;

    let content = fs::read_to_string(&output_path)?;
    let expected_content = "name,units_available,calories_per_unit,perishability_score\nCanned Soup,5,150,1\n";
    assert_eq!(content, expected_content);

    Ok(())
}

#[test]
fn test_perishability_sorting() {
    let mut items = vec![
        RationItem {
            name: "Item A".to_string(),
            calories_per_unit: 100,
            units_available: 1,
            perishability_score: 3,
        },
        RationItem {
            name: "Item B".to_string(),
            calories_per_unit: 200,
            units_available: 1,
            perishability_score: 1,
        },
        RationItem {
            name: "Item C".to_string(),
            calories_per_unit: 50,
            units_available: 1,
            perishability_score: 5,
        },
        RationItem {
            name: "Item D".to_string(),
            calories_per_unit: 150,
            units_available: 1,
            perishability_score: 3,
        },
    ];
    let target = 1000;

    let (plan, _remaining_items) = calculate_ration_plan(&mut items, target);

    // Expected order of consumption: C (5), A (3, higher cal), D (3, lower cal), B (1)
    assert_eq!(plan.consumed_items[0].0, "Item C");
    assert_eq!(plan.consumed_items[1].0, "Item A");
    assert_eq!(plan.consumed_items[2].0, "Item D");
    assert_eq!(plan.consumed_items[3].0, "Item B");
}
