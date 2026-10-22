use assert_cmd::prelude::*;
use predicates::prelude::*;
use std::process::Command;
use std::io::Write;
use tempfile::NamedTempFile;

#[test]
fn test_sort_descending() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: We need to simulate file input for the CLI tool.
    // Creating a temporary file allows us to provide controlled input
    // without relying on actual filesystem state or network.
    let mut file = NamedTempFile::new()?;
    writeln!(file, "Water,10,Common,Pristine")?;
    writeln!(file, "Medical Kit,8,Rare,Worn")?;
    writeln!(file, "Rusty Spoon,1,Common,Broken")?;
    writeln!(file, "Ancient AI Core,20,Legendary,Pristine")?;
    let input_path = file.path();

    let mut cmd = Command::cargo_bin("nightly-scavenge-sorter")?;
    cmd.arg("-i").arg(input_path);

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(
            "--- Scavenged Item Prioritization ---\n\
            [120.00] Ancient AI Core (Utility: 20, Rarity: Legendary, Condition: Pristine)\n\
            [20.00] Medical Kit (Utility: 8, Rarity: Rare, Condition: Worn)\n\
            [12.00] Water (Utility: 10, Rarity: Common, Condition: Pristine)\n\
            [0.30] Rusty Spoon (Utility: 1, Rarity: Common, Condition: Broken)\n"
        ));

    Ok(())
}

#[test]
fn test_sort_ascending() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Similar to the descending test, we use a temporary file
    // to provide deterministic input for the CLI tool.
    // This ensures the sorting logic works correctly for both orders.
    let mut file = NamedTempFile::new()?;
    writeln!(file, "Water,10,Common,Pristine")?;
    writeln!(file, "Medical Kit,8,Rare,Worn")?;
    writeln!(file, "Rusty Spoon,1,Common,Broken")?;
    writeln!(file, "Ancient AI Core,20,Legendary,Pristine")?;
    let input_path = file.path();

    let mut cmd = Command::cargo_bin("nightly-scavenge-sorter")?;
    cmd.arg("-i").arg(input_path).arg("-o").arg("asc");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains(
            "--- Scavenged Item Prioritization ---\n\
            [0.30] Rusty Spoon (Utility: 1, Rarity: Common, Condition: Broken)\n\
            [12.00] Water (Utility: 10, Rarity: Common, Condition: Pristine)\n\
            [20.00] Medical Kit (Utility: 8, Rarity: Rare, Condition: Worn)\n\
            [120.00] Ancient AI Core (Utility: 20, Rarity: Legendary, Condition: Pristine)\n"
        ));

    Ok(())
}

#[test]
fn test_invalid_input_file() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: Testing with a non-existent file path ensures the tool
    // handles file I/O errors gracefully without external dependencies.
    let mut cmd = Command::cargo_bin("nightly-scavenge-sorter")?;
    cmd.arg("-i").arg("non_existent_file.txt");

    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("No such file or directory"));

    Ok(())
}

#[test]
fn test_malformed_line_warning() -> Result<(), Box<dyn std::error::Error>> {
    // Mock rationale: A temporary file with mixed valid and invalid lines
    // allows us to verify that the tool logs warnings for malformed input
    // but continues processing valid lines. This ensures robustness.
    let mut file = NamedTempFile::new()?;
    writeln!(file, "Valid Item,5,Common,Worn")?;
    writeln!(file, "Invalid Line,5,Common")?; // Malformed
    writeln!(file, "Another Valid,10,Rare,Pristine")?;
    let input_path = file.path();

    let mut cmd = Command::cargo_bin("nightly-scavenge-sorter")?;
    cmd.arg("-i").arg(input_path);

    cmd.assert()
        .success() // Should still succeed if some lines are valid
        .stderr(predicate::str::contains("Warning: Could not parse line 'Invalid Line,5,Common': Invalid item format: expected 4 parts, got 3"))
        .stdout(predicate::str::contains(
            "--- Scavenged Item Prioritization ---\n\
            [30.00] Another Valid (Utility: 10, Rarity: Rare, Condition: Pristine)\n\
            [5.00] Valid Item (Utility: 5, Rarity: Common, Condition: Worn)\n"
        ));

    Ok(())
}
