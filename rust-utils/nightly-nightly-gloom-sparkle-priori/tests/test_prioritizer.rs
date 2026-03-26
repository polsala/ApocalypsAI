use super::{run, Item};
use std::io::Cursor;

// Mock rationale: Using `Cursor` to simulate file input from a string for deterministic and offline testing.

#[test]
fn test_item_survival_score_calculation() {
    let mut item = Item {
        item_name: "Test Item".to_string(),
        gloom_factor: 5,
        sparkle_potential: 7,
        survival_score: 0,
    };
    item.calculate_survival_score();
    assert_eq!(item.survival_score, 7 - 5 + 10); // 12

    let mut item2 = Item {
        item_name: "Another Item".to_string(),
        gloom_factor: 1,
        sparkle_potential: 10,
        survival_score: 0,
    };
    item2.calculate_survival_score();
    assert_eq!(item2.survival_score, 10 - 1 + 10); // 19

    let mut item3 = Item {
        item_name: "Worst Item".to_string(),
        gloom_factor: 10,
        sparkle_potential: 1,
        survival_score: 0,
    };
    item3.calculate_survival_score();
    assert_eq!(item3.survival_score, 1 - 10 + 10); // 1
}

#[test]
fn test_item_factor_validation_valid() {
    let item = Item {
        item_name: "Valid Item".to_string(),
        gloom_factor: 5,
        sparkle_potential: 7,
        survival_score: 0,
    };
    assert!(item.validate_factors().is_ok());

    let item_min = Item {
        item_name: "Min Item".to_string(),
        gloom_factor: 1,
        sparkle_potential: 1,
        survival_score: 0,
    };
    assert!(item_min.validate_factors().is_ok());

    let item_max = Item {
        item_name: "Max Item".to_string(),
        gloom_factor: 10,
        sparkle_potential: 10,
        survival_score: 0,
    };
    assert!(item_max.validate_factors().is_ok());
}

#[test]
fn test_item_factor_validation_invalid_gloom() {
    let item_low_gloom = Item {
        item_name: "Low Gloom".to_string(),
        gloom_factor: 0,
        sparkle_potential: 5,
        survival_score: 0,
    };
    assert!(item_low_gloom.validate_factors().is_err());

    let item_high_gloom = Item {
        item_name: "High Gloom".to_string(),
        gloom_factor: 11,
        sparkle_potential: 5,
        survival_score: 0,
    };
    assert!(item_high_gloom.validate_factors().is_err());
}

#[test]
fn test_item_factor_validation_invalid_sparkle() {
    let item_low_sparkle = Item {
        item_name: "Low Sparkle".to_string(),
        gloom_factor: 5,
        sparkle_potential: 0,
        survival_score: 0,
    };
    assert!(item_low_sparkle.validate_factors().is_err());

    let item_high_sparkle = Item {
        item_name: "High Sparkle".to_string(),
        gloom_factor: 5,
        sparkle_potential: 11,
        survival_score: 0,
    };
    assert!(item_high_sparkle.validate_factors().is_err());
}

#[test]
fn test_run_with_valid_csv_input() {
    let csv_data = "Rusty Spanner,3,5\nCan of Dehydrated Noodles,2,7\nBroken Geiger Counter,8,1\nMap to the Whispering Wastes,5,9\nSinging Wind Chimes,1,3\nMutated Radish Seeds,6,4";
    let reader = Cursor::new(csv_data);

    let mut buffer = Vec::new();
    // Mock rationale: Redirect stdout to a buffer to capture the output for assertion.
    // This ensures the test is deterministic and doesn't rely on actual console output.
    let original_stdout = io::stdout();
    let mut captured_stdout = Cursor::new(buffer);
    io::set_stdout(Box::new(captured_stdout.get_mut())).unwrap();

    let result = run(reader);
    assert!(result.is_ok());

    // Restore stdout
    io::set_stdout(Box::new(original_stdout)).unwrap();

    let output = String::from_utf8(captured_stdout.into_inner()).unwrap();

    assert!(output.contains("Prioritized Scavenged Items:"));
    assert!(output.contains("1. Map to the Whispering Wastes (Survival Score: 14, Gloom: 5, Sparkle: 9)"));
    assert!(output.contains("2. Can of Dehydrated Noodles (Survival Score: 15, Gloom: 2, Sparkle: 7)"));
    assert!(output.contains("3. Rusty Spanner (Survival Score: 12, Gloom: 3, Sparkle: 5)"));
    assert!(output.contains("4. Singing Wind Chimes (Survival Score: 12, Gloom: 1, Sparkle: 3)"));
    assert!(output.contains("5. Mutated Radish Seeds (Survival Score: 8, Gloom: 6, Sparkle: 4)"));
    assert!(output.contains("6. Broken Geiger Counter (Survival Score: 3, Gloom: 8, Sparkle: 1)"));

    // Verify order (scores: Map=14, Noodles=15, Spanner=12, Chimes=12, Radish=8, Geiger=3)
    // Note: Noodles should be first, then Map, then Spanner/Chimes (order between same scores is stable but not guaranteed specific)
    let lines: Vec<&str> = output.lines().collect();
    assert!(lines[2].contains("Can of Dehydrated Noodles")); // Score 15
    assert!(lines[3].contains("Map to the Whispering Wastes")); // Score 14
    // The next two could be in either order due to same score, but they should be there
    assert!(lines[4].contains("Rusty Spanner") || lines[4].contains("Singing Wind Chimes"));
    assert!(lines[5].contains("Rusty Spanner") || lines[5].contains("Singing Wind Chimes"));
    assert!(lines[6].contains("Mutated Radish Seeds")); // Score 8
    assert!(lines[7].contains("Broken Geiger Counter")); // Score 3
}

#[test]
fn test_run_with_invalid_csv_format() {
    let csv_data = "Item1,3,5\nItem2,invalid,7";
    let reader = Cursor::new(csv_data);

    let result = run(reader);
    assert!(result.is_err());
    let err_msg = result.unwrap_err().to_string();
    assert!(err_msg.contains("failed to parse field"));
}

#[test]
fn test_run_with_invalid_factor_range() {
    let csv_data = "Item1,3,5\nItem2,0,7"; // Gloom factor 0 is invalid
    let reader = Cursor::new(csv_data);

    let result = run(reader);
    assert!(result.is_err());
    let err_msg = result.unwrap_err().to_string();
    assert!(err_msg.contains("Gloom factor for 'Item2' is out of range (1-10): 0"));
}

#[test]
fn test_run_with_empty_input() {
    let csv_data = "";
    let reader = Cursor::new(csv_data);

    let mut buffer = Vec::new();
    let original_stdout = io::stdout();
    let mut captured_stdout = Cursor::new(buffer);
    io::set_stdout(Box::new(captured_stdout.get_mut())).unwrap();

    let result = run(reader);
    assert!(result.is_ok());

    io::set_stdout(Box::new(original_stdout)).unwrap();
    let output = String::from_utf8(captured_stdout.into_inner()).unwrap();

    assert!(output.contains("Prioritized Scavenged Items:"));
    assert!(!output.contains("1.")); // No items should be listed
}
