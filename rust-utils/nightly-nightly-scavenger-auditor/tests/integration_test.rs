use std::process::Command;
use std::io::Write;
use tempfile::NamedTempFile; // Need to add tempfile to Cargo.toml dev-dependencies

// Mock rationale: We need to test the CLI tool's behavior with different file inputs.
// Creating temporary files allows us to simulate file system interactions deterministically
// without relying on actual files that might change or not exist.

#[test]
fn test_perfect_match() -> Result<(), Box<dyn std::error::Error>> {
    let mut manifest_file = NamedTempFile::new()?;
    writeln!(manifest_file, "Water Bottle")?;
    writeln!(manifest_file, "Ration Pack")?;
    writeln!(manifest_file, "First Aid Kit")?;
    let manifest_path = manifest_file.path().to_str().unwrap();

    let mut scavenged_file = NamedTempFile::new()?;
    writeln!(scavenged_file, "Water Bottle")?;
    writeln!(scavenged_file, "Ration Pack")?;
    writeln!(scavenged_file, "First Aid Kit")?;
    let scavenged_path = scavenged_file.path().to_str().unwrap();

    let output = Command::new("cargo")
        .args(&["run", "--", manifest_path, scavenged_path])
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(output.status.success());
    assert!(stdout.contains("All manifest items accounted for!"));
    assert!(stdout.contains("No surplus items found!"));
    assert!(stdout.contains("Manifest perfectly matched!"));
    assert!(stderr.is_empty());

    Ok(())
}

#[test]
fn test_missing_items() -> Result<(), Box<dyn std::error::Error>> {
    let mut manifest_file = NamedTempFile::new()?;
    writeln!(manifest_file, "Water Bottle")?;
    writeln!(manifest_file, "Ration Pack")?;
    writeln!(manifest_file, "First Aid Kit")?;
    let manifest_path = manifest_file.path().to_str().unwrap();

    let mut scavenged_file = NamedTempFile::new()?;
    writeln!(scavenged_file, "Water Bottle")?;
    writeln!(scavenged_file, "First Aid Kit")?; // Ration Pack is missing
    let scavenged_path = scavenged_file.path().to_str().unwrap();

    let output = Command::new("cargo")
        .args(&["run", "--", manifest_path, scavenged_path])
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Missing Items (in manifest, not enough scavenged):"));
    assert!(stdout.contains("  - Ration Pack (1 missing)"));
    assert!(stdout.contains("No surplus items found!"));
    assert!(stderr.is_empty());

    Ok(())
}

#[test]
fn test_surplus_items() -> Result<(), Box<dyn std::error::Error>> {
    let mut manifest_file = NamedTempFile::new()?;
    writeln!(manifest_file, "Water Bottle")?;
    writeln!(manifest_file, "Ration Pack")?;
    let manifest_path = manifest_file.path().to_str().unwrap();

    let mut scavenged_file = NamedTempFile::new()?;
    writeln!(scavenged_file, "Water Bottle")?;
    writeln!(scavenged_file, "Ration Pack")?;
    writeln!(scavenged_file, "Scrap Metal")?; // Surplus item
    let scavenged_path = scavenged_file.path().to_str().unwrap();

    let output = Command::new("cargo")
        .args(&["run", "--", manifest_path, scavenged_path])
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(output.status.success());
    assert!(stdout.contains("All manifest items accounted for!"));
    assert!(stdout.contains("Surplus Items (scavenged, not in manifest or too many):"));
    assert!(stdout.contains("  - Scrap Metal (1 surplus)"));
    assert!(stderr.is_empty());

    Ok(())
}

#[test]
fn test_mixed_discrepancies() -> Result<(), Box<dyn std::error::Error>> {
    let mut manifest_file = NamedTempFile::new()?;
    writeln!(manifest_file, "Water Bottle")?;
    writeln!(manifest_file, "Ration Pack")?;
    writeln!(manifest_file, "First Aid Kit")?;
    let manifest_path = manifest_file.path().to_str().unwrap();

    let mut scavenged_file = NamedTempFile::new()?;
    writeln!(scavenged_file, "Water Bottle")?;
    writeln!(scavenged_file, "Scrap Metal")?; // Surplus
    let scavenged_path = scavenged_file.path().to_str().unwrap();

    let output = Command::new("cargo")
        .args(&["run", "--", manifest_path, scavenged_path])
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Missing Items (in manifest, not enough scavenged):"));
    assert!(stdout.contains("  - Ration Pack (1 missing)"));
    assert!(stdout.contains("  - First Aid Kit (1 missing)"));
    assert!(stdout.contains("Surplus Items (scavenged, not in manifest or too many):"));
    assert!(stdout.contains("  - Scrap Metal (1 surplus)"));
    assert!(stderr.is_empty());

    Ok(())
}

#[test]
fn test_duplicate_items() -> Result<(), Box<dyn std::error::Error>> {
    let mut manifest_file = NamedTempFile::new()?;
    writeln!(manifest_file, "Water Bottle")?;
    writeln!(manifest_file, "Water Bottle")?; // Two water bottles needed
    writeln!(manifest_file, "Ration Pack")?;
    let manifest_path = manifest_file.path().to_str().unwrap();

    let mut scavenged_file = NamedTempFile::new()?;
    writeln!(scavenged_file, "Water Bottle")?; // Only one found
    writeln!(scavenged_file, "Ration Pack")?;
    writeln!(scavenged_file, "Scrap Metal")?; // Surplus
    let scavenged_path = scavenged_file.path().to_str().unwrap();

    let output = Command::new("cargo")
        .args(&["run", "--", manifest_path, scavenged_path])
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Missing Items (in manifest, not enough scavenged):"));
    assert!(stdout.contains("  - Water Bottle (1 missing)")); // One Water Bottle is missing
    assert!(stdout.contains("Surplus Items (scavenged, not in manifest or too many):"));
    assert!(stdout.contains("  - Scrap Metal (1 surplus)"));
    assert!(stderr.is_empty());

    Ok(())
}

#[test]
fn test_file_not_found() -> Result<(), Box<dyn std::error::Error>> {
    let manifest_path = "non_existent_manifest.txt";
    let mut scavenged_file = NamedTempFile::new()?;
    writeln!(scavenged_file, "Water Bottle")?;
    let scavenged_path = scavenged_file.path().to_str().unwrap();

    let output = Command::new("cargo")
        .args(&["run", "--", manifest_path, scavenged_path])
        .output()?;

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(!output.status.success()); // Should fail
    assert!(stderr.contains("No such file or directory") || stderr.contains("os error 2")); // Specific error message might vary by OS
    Ok(())
}
