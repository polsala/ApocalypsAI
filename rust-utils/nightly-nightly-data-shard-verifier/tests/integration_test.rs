use assert_cmd::prelude::*;
use predicates::prelude::*;
use std::process::Command;
use std::fs;
use std::io::Write;
use tempfile::tempdir;

// Mock rationale: We are testing the CLI tool's behavior with actual files
// on the filesystem, which is the core functionality. Using tempfile ensures
// these files are isolated and cleaned up, making tests deterministic and offline.

#[test]
fn test_file_not_found() -> Result<(), Box<dyn std::error::Error>> {
    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg("non_existent_file.txt");
    cmd.assert()
        .failure()
        .stderr(predicate::str::contains("Error: Path does not exist"));
    Ok(())
}

#[test]
fn test_empty_file() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("empty.txt");
    fs::File::create(&file_path)?; // Create an empty file

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&file_path);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")) // SHA256 of empty string
        .stdout(predicate::str::contains("Identified Type: Plain Text")); // Empty file is considered plain text by our simple heuristic
    Ok(())
}

#[test]
fn test_text_file_checksum_and_type() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("test.txt");
    fs::write(&file_path, "Hello, ApocalypsAI!")?;
    // SHA256 of "Hello, ApocalypsAI!" is 09470125792949a461322744383187212629618147d33742416f40398014841d

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&file_path);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("SHA256: 09470125792949a461322744383187212629618147d33742416f40398014841d"))
        .stdout(predicate::str::contains("Identified Type: Plain Text"));
    Ok(())
}

#[test]
fn test_text_file_checksum_match() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("match.txt");
    fs::write(&file_path, "Integrity check!")?;
    let expected_checksum = "722880155b1184711f715104250260424610191834164b4c73331b2649060000"; // SHA256 of "Integrity check!"

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&file_path)
        .arg("-e").arg(expected_checksum);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Checksum: MATCHES expected!"));
    Ok(())
}

#[test]
fn test_text_file_checksum_mismatch() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("mismatch.txt");
    fs::write(&file_path, "Wrong content.")?;
    let expected_checksum = "a_fake_checksum_for_mismatch";

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&file_path)
        .arg("-e").arg(expected_checksum);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Checksum: MISMATCH!"));
    Ok(())
}

#[test]
fn test_directory_processing() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let sub_dir = dir.path().join("data_shards");
    fs::create_dir(&sub_dir)?;

    let file1_path = sub_dir.join("file1.txt");
    fs::write(&file1_path, "Content one.")?;
    let file2_path = sub_dir.join("file2.txt");
    fs::write(&file2_path, "Content two.")?;

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&sub_dir);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains(format!("Processing: {}", file1_path.display())))
        .stdout(predicate::str::contains(format!("Processing: {}", file2_path.display())));
    Ok(())
}

#[test]
fn test_png_identification() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("image.png");
    // PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
    let png_header = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A];
    let mut file = fs::File::create(&file_path)?;
    file.write_all(&png_header)?;

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&file_path);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Identified Type: PNG Image"));
    Ok(())
}

#[test]
fn test_jpeg_identification() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("image.jpg");
    // JPEG magic bytes (JFIF): FF D8 FF E0
    let jpeg_header = [0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46];
    let mut file = fs::File::create(&file_path)?;
    file.write_all(&jpeg_header)?;

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&file_path);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Identified Type: JPEG Image"));
    Ok(())
}

#[test]
fn test_pdf_identification() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("doc.pdf");
    // PDF magic bytes: %PDF
    let pdf_header = b"%PDF-1.4\n";
    let mut file = fs::File::create(&file_path)?;
    file.write_all(pdf_header)?;

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&file_path);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Identified Type: PDF Document"));
    Ok(())
}

#[test]
fn test_zip_identification() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("archive.zip");
    // ZIP magic bytes: PK\x03\x04
    let zip_header = [0x50, 0x4B, 0x03, 0x04, 0x14, 0x00, 0x06, 0x00];
    let mut file = fs::File::create(&file_path)?;
    file.write_all(&zip_header)?;

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&file_path);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Identified Type: ZIP Archive"));
    Ok(())
}

#[test]
fn test_unknown_file_type() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("unknown.bin");
    fs::write(&file_path, &[0x01, 0x02, 0x03, 0x04, 0x05])?; // Arbitrary bytes not matching known types

    let mut cmd = Command::cargo_bin("nightly-data-shard-verifier")?;
    cmd.arg("-p").arg(&file_path);
    cmd.assert()
        .success()
        .stdout(predicate::str::contains("Identified Type: Unknown"));
    Ok(())
}
