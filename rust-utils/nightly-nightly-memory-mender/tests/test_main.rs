use assert_cmd::Command;
use predicates::prelude::*;
use std::fs;
use std::io::Write;
use std::path::PathBuf;
use tempfile::NamedTempFile; // # Mock rationale: Using NamedTempFile to create temporary files for testing file I/O operations. This ensures tests are isolated, deterministic, and do not affect the actual filesystem or rely on external resources.

#[test]
fn test_no_corruption_file() {
    let mut file = NamedTempFile::new().unwrap();
    writeln!(file, "This is a clean file.").unwrap();
    let input_path = file.path().to_owned();

    let mut cmd = Command::cargo_bin("nightly-memory-mender").unwrap();
    cmd.arg("--input").arg(&input_path)
        .assert()
        .success()
        .stdout(predicate::str::contains("No corruptions detected").and(predicate::str::contains(&format!("{:?}", input_path))));

    let content = fs::read_to_string(&input_path).unwrap();
    assert_eq!(content, "This is a clean file.\n"); // Original content should remain
}

#[test]
fn test_with_corruption_and_overwrite() {
    let mut file = NamedTempFile::new().unwrap();
    writeln!(file, "Corrupt\x00Data\u{FFFD}Here\x01").unwrap();
    let input_path = file.path().to_owned();
    let backup_path = input_path.with_extension("bak");

    let mut cmd = Command::cargo_bin("nightly-memory-mender").unwrap();
    cmd.arg("--input").arg(&input_path)
        .assert()
        .success()
        .stdout(predicate::str::contains("Detected and mended 3 instances of corruption."))
        .stdout(predicate::str::contains(format!("Creating backup of original file at {:?}", backup_path)))
        .stdout(predicate::str::contains(format!("Mending complete. Output written to {:?}", input_path)));

    let mended_content = fs::read_to_string(&input_path).unwrap();
    assert_eq!(mended_content, "Corrupt[MENDED]Data[MENDED]Here[MENDED]\n");

    let original_backup_content = fs::read_to_string(&backup_path).unwrap();
    assert_eq!(original_backup_content, "Corrupt\x00Data\u{FFFD}Here\x01\n");

    // Clean up backup file
    fs::remove_file(&backup_path).unwrap();
}

#[test]
fn test_with_corruption_and_output_file() {
    let mut input_file = NamedTempFile::new().unwrap();
    writeln!(input_file, "Corrupt\x00Data\u{FFFD}Here\x01").unwrap();
    let input_path = input_file.path().to_owned();

    let output_file = NamedTempFile::new().unwrap();
    let output_path = output_file.path().to_owned();

    let mut cmd = Command::cargo_bin("nightly-memory-mender").unwrap();
    cmd.arg("--input").arg(&input_path)
        .arg("--output").arg(&output_path)
        .assert()
        .success()
        .stdout(predicate::str::contains("Detected and mended 3 instances of corruption."))
        .stdout(predicate::str::contains(format!("Mending complete. Output written to {:?}", output_path)));

    let mended_content = fs::read_to_string(&output_path).unwrap();
    assert_eq!(mended_content, "Corrupt[MENDED]Data[MENDED]Here[MENDED]\n");

    let original_input_content = fs::read_to_string(&input_path).unwrap();
    assert_eq!(original_input_content, "Corrupt\x00Data\u{FFFD}Here\x01\n"); // Original input should be untouched

    // Clean up files
    fs::remove_file(&input_path).unwrap();
    fs::remove_file(&output_path).unwrap();
}

#[test]
fn test_dry_run() {
    let mut file = NamedTempFile::new().unwrap();
    writeln!(file, "Corrupt\x00Data\u{FFFD}Here\x01").unwrap();
    let input_path = file.path().to_owned();

    let mut cmd = Command::cargo_bin("nightly-memory-mender").unwrap();
    cmd.arg("--input").arg(&input_path)
        .arg("--dry-run")
        .assert()
        .success()
        .stdout(predicate::str::contains("Detected and mended 3 instances of corruption."))
        .stdout(predicate::str::contains("Dry run complete. No changes written to disk."))
        .stdout(predicate::str::contains("Corrupt[MENDED]Data[MENDED]Here[MENDED]"));

    let content = fs::read_to_string(&input_path).unwrap();
    assert_eq!(content, "Corrupt\x00Data\u{FFFD}Here\x01\n"); // Original content should remain unchanged
}

#[test]
fn test_custom_placeholder() {
    let mut file = NamedTempFile::new().unwrap();
    writeln!(file, "Corrupt\x00Data").unwrap();
    let input_path = file.path().to_owned();

    let mut cmd = Command::cargo_bin("nightly-memory-mender").unwrap();
    cmd.arg("--input").arg(&input_path)
        .arg("--placeholder").arg("VOID")
        .assert()
        .success()
        .stdout(predicate::str::contains("Detected and mended 1 instances of corruption."));

    let mended_content = fs::read_to_string(&input_path).unwrap();
    assert_eq!(mended_content, "CorruptVOIDData\n");

    // Clean up backup file
    fs::remove_file(input_path.with_extension("bak")).unwrap();
}

#[test]
fn test_input_file_not_found() {
    let non_existent_path = PathBuf::from("non_existent_file_12345.txt");

    let mut cmd = Command::cargo_bin("nightly-memory-mender").unwrap();
    cmd.arg("--input").arg(&non_existent_path)
        .assert()
        .failure()
        .stderr(predicate::str::contains("Error: Input file not found"));
}
