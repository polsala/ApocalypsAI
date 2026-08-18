use assert_cmd::Command;
use predicates::prelude::*;
use tempfile::NamedTempFile;
use std::io::{self, Write};

// Mock rationale: We create temporary CSV files to simulate user input
// and capture stdout to verify the program's output, ensuring tests are
// deterministic and offline without relying on actual file system state
// or external processes.

#[test]
fn test_basic_packing() -> Result<(), Box<dyn std::error::Error>> {
    let mut file = NamedTempFile::new()?;
    writeln!(file, "name,value,weight,volume")?;
    writeln!(file, "Rusty Spoon,1,0.1,0.05")?;
    writeln!(file, "Can of Beans,10,0.5,0.3")?;
    writeln!(file, "Water Bottle (empty),5,0.2,1.0")?;
    writeln!(file, "First Aid Kit,20,1.0,0.5")?;
    writeln!(file, "Tattered Blanket,8,2.0,5.0")?;
    writeln!(file, "Multi-tool,15,0.3,0.1")?;
    let file_path = file.path().to_str().unwrap();

    let mut cmd = Command::cargo_bin("nightly-scav-manifest-opt")?;
    cmd.arg("--file").arg(file_path)
       .arg("--max-weight").arg("2.0")
       .arg("--max-volume").arg("2.0");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("--- Scavenger Manifest Optimization Report ---"))
        .stdout(predicate::str::contains("Container Capacity: Max Weight = 2.00kg, Max Volume = 2.00L"))
        .stdout(predicate::str::contains("Packed Items:"))
        .stdout(predicate::str::contains("  - Multi-tool (Value: 15, Weight: 0.30kg, Volume: 0.10L)"))
        .stdout(predicate::str::contains("  - Water Bottle (empty) (Value: 5, Weight: 0.20kg, Volume: 1.00L)"))
        .stdout(predicate::str::contains("  - Can of Beans (Value: 10, Weight: 0.50kg, Volume: 0.30L)"))
        .stdout(predicate::str::contains("  - First Aid Kit (Value: 20, Weight: 1.00kg, Volume: 0.50L)"))
        .stdout(predicate::str::contains("Total Packed Value: 50"))
        .stdout(predicate::str::contains("Total Packed Weight: 2.00kg"))
        .stdout(predicate::str::contains("Total Packed Volume: 1.90L"));

    Ok(())
}

#[test]
fn test_no_items_packed_if_constraints_too_low() -> Result<(), Box<dyn std::error::Error>> {
    let mut file = NamedTempFile::new()?;
    writeln!(file, "name,value,weight,volume")?;
    writeln!(file, "Heavy Rock,1,10.0,10.0")?;
    let file_path = file.path().to_str().unwrap();

    let mut cmd = Command::cargo_bin("nightly-scav-manifest-opt")?;
    cmd.arg("--file").arg(file_path)
       .arg("--max-weight").arg("1.0")
       .arg("--max-volume").arg("1.0");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("No items could be packed within the given constraints."));

    Ok(())
}

#[test]
fn test_empty_input_file() -> Result<(), Box<dyn std::error::Error>> {
    let mut file = NamedTempFile::new()?;
    writeln!(file, "name,value,weight,volume")?; // Only header
    let file_path = file.path().to_str().unwrap();

    let mut cmd = Command::cargo_bin("nightly-scav-manifest-opt")?;
    cmd.arg("--file").arg(file_path)
       .arg("--max-weight").arg("10.0")
       .arg("--max-volume").arg("10.0");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("No items could be packed within the given constraints."));

    Ok(())
}

#[test]
fn test_file_not_found_error() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("nightly-scav-manifest-opt")?;
    cmd.arg("--file").arg("non_existent_file.csv")
       .arg("--max-weight").arg("10.0")
       .arg("--max-volume").arg("10.0");

    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("No such file or directory"));

    Ok(())
}

#[test]
fn test_packing_with_different_constraints() -> Result<(), Box<dyn std::error::Error>> {
    let mut file = NamedTempFile::new()?;
    writeln!(file, "name,value,weight,volume")?;
    writeln!(file, "Small Battery,5,0.1,0.05")?;
    writeln!(file, "Large Battery,15,0.5,0.2")?;
    writeln!(file, "Heavy Tool,20,2.0,0.8")?;
    let file_path = file.path().to_str().unwrap();

    let mut cmd = Command::cargo_bin("nightly-scav-manifest-opt")?;
    cmd.arg("--file").arg(file_path)
       .arg("--max-weight").arg("0.6")
       .arg("--max-volume").arg("0.3");

    cmd.assert()
        .success()
        .stdout(predicate::str::contains("  - Small Battery (Value: 5, Weight: 0.10kg, Volume: 0.05L)"))
        .stdout(predicate::str::contains("  - Large Battery (Value: 15, Weight: 0.50kg, Volume: 0.20L)"))
        .stdout(predicate::str::contains("Total Packed Value: 20"))
        .stdout(predicate::str::contains("Total Packed Weight: 0.60kg"))
        .stdout(predicate::str::contains("Total Packed Volume: 0.25L"));

    Ok(())
}
