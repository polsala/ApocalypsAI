use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use std::io::Write;

// Mock rationale: These tests use a temporary, in-memory CSV file for item data
// to ensure determinism and avoid external dependencies or file system side effects.

#[test]
fn test_basic_optimization() -> Result<(), Box<dyn std::error::Error>> {
    let items_csv = "name,weight,value\nRusty Can Opener,1,2\nMutant Rat Jerky,2,5\nPre-War Comic Book,1,3\nIntact Water Filter,5,10\nBroken Radio,3,1\nMedical Kit,4,8\n";
    let temp_dir = tempfile::tempdir()?;
    let file_path = temp_dir.path().join("items.csv");
    fs::write(&file_path, items_csv)?;

    let mut cmd = Command::cargo_bin("nightly-scavenger-pack-opt")?;
    cmd.arg("--max-weight").arg("7");
    cmd.arg("--items-file").arg(&file_path);

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Optimizing for max weight: 7"))
        .stdout(predicate::str::contains("Selected Items:"))
        .stdout(predicate::str::contains("- Mutant Rat Jerky (Weight: 2, Value: 5)"))
        .stdout(predicate::str::contains("- Pre-War Comic Book (Weight: 1, Value: 3)"))
        .stdout(predicate::str::contains("- Medical Kit (Weight: 4, Value: 8)"))
        .stdout(predicate::str::contains("Total Weight: 7"))
        .stdout(predicate::str::contains("Total Value: 16"));

    Ok(())
}

#[test]
fn test_no_items_selected_if_too_heavy() -> Result<(), Box<dyn std::error::Error>> {
    let items_csv = "name,weight,value\nHeavy Armor,10,20\nLarge Generator,50,100\n";
    let temp_dir = tempfile::tempdir()?;
    let file_path = temp_dir.path().join("items.csv");
    fs::write(&file_path, items_csv)?;

    let mut cmd = Command::cargo_bin("nightly-scavenger-pack-opt")?;
    cmd.arg("--max-weight").arg("5");
    cmd.arg("--items-file").arg(&file_path);

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Optimizing for max weight: 5"))
        .stdout(predicate::str::contains("Selected Items:"))
        .stdout(predicate::str::contains("  (No items selected)"))
        .stdout(predicate::str::contains("Total Weight: 0"))
        .stdout(predicate::str::contains("Total Value: 0"));

    Ok(())
}

#[test]
fn test_empty_items_file() -> Result<(), Box<dyn std::error::Error>> {
    let items_csv = "name,weight,value\n"; // Only header
    let temp_dir = tempfile::tempdir()?;
    let file_path = temp_dir.path().join("items.csv");
    fs::write(&file_path, items_csv)?;

    let mut cmd = Command::cargo_bin("nightly-scavenger-pack-opt")?;
    cmd.arg("--max-weight").arg("10");
    cmd.arg("--items-file").arg(&file_path);

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Optimizing for max weight: 10"))
        .stdout(predicate::str::contains("Selected Items:"))
        .stdout(predicate::str::contains("  (No items selected)"))
        .stdout(predicate::str::contains("Total Weight: 0"))
        .stdout(predicate::str::contains("Total Value: 0"));

    Ok(())
}

#[test]
fn test_single_item_selection() -> Result<(), Box<dyn std::error::Error>> {
    let items_csv = "name,weight,value\nSuper Valuable Gem,3,100\nSmall Rock,1,1\n";
    let temp_dir = tempfile::tempdir()?;
    let file_path = temp_dir.path().join("items.csv");
    fs::write(&file_path, items_csv)?;

    let mut cmd = Command::cargo_bin("nightly-scavenger-pack-opt")?;
    cmd.arg("--max-weight").arg("3");
    cmd.arg("--items-file").arg(&file_path);

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Optimizing for max weight: 3"))
        .stdout(predicate::str::contains("Selected Items:"))
        .stdout(predicate::str::contains("- Super Valuable Gem (Weight: 3, Value: 100)"))
        .stdout(predicate::str::contains("Total Weight: 3"))
        .stdout(predicate::str::contains("Total Value: 100"));

    Ok(())
}

#[test]
fn test_file_not_found() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("nightly-scavenger-pack-opt")?;
    cmd.arg("--max-weight").arg("10");
    cmd.arg("--items-file").arg("non_existent_file.csv");

    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("No such file or directory"));

    Ok(())
}
