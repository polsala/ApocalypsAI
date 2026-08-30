use std::process::Command;
use std::io::Write;
use std::fs;
use std::path::PathBuf;
use tempfile::NamedTempFile; // For creating temporary files

// Mock rationale: We create temporary binary files with controlled content to ensure deterministic and offline testing.
// This allows us to precisely control the input and verify the output without relying on external file systems or network resources.

#[test]
fn test_basic_pattern_extraction() {
    let mut temp_file = NamedTempFile::new().expect("Failed to create temp file");
    let file_path = temp_file.path().to_path_buf();

    // Create a binary file with repeating patterns
    // Pattern 1: 01 02 03 04 (repeats 3 times)
    // Pattern 2: FF FF FF FF (repeats 2 times)
    // Pattern 3: 00 00 00 00 (repeats 1 time)
    // Some unique bytes
    let content = vec![
        0x01, 0x02, 0x03, 0x04, // P1
        0x05, 0x06, 0x07, 0x08,
        0x01, 0x02, 0x03, 0x04, // P1
        0xFF, 0xFF, 0xFF, 0xFF, // P2
        0x09, 0x0A, 0x0B, 0x0C,
        0x01, 0x02, 0x03, 0x04, // P1
        0xFF, 0xFF, 0xFF, 0xFF, // P2
        0x00, 0x00, 0x00, 0x00, // P3
        0xDE, 0xAD, 0xBE, 0xEF,
    ];
    temp_file.write_all(&content).expect("Failed to write to temp file");
    temp_file.flush().expect("Failed to flush temp file");

    let output = Command::new("cargo")
        .arg("run")
        .arg("--quiet")
        .arg("--")
        .arg("-f")
        .arg(&file_path)
        .arg("-p")
        .arg("4") // Pattern length 4
        .arg("-t")
        .arg("3") // Top 3 patterns
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(output.status.success(), "Command failed with stdout: {}\nstderr: {}", stdout, stderr);

    // Check for expected patterns and counts
    assert!(stdout.contains("Pattern: 01 02 03 04 (Count: 3) -> Cryptic Resonance: An unknown signal from the data depths."));
    assert!(stdout.contains("Pattern: FF FF FF FF (Count: 2) -> Echoes of the Old World: Remnants of forgotten data."));
    assert!(stdout.contains("Pattern: 00 00 00 00 (Count: 1) -> Silence of the Void: A deep, unsettling calm."));

    // Ensure the order is generally correct (highest count first)
    let p1_idx = stdout.find("01 02 03 04 (Count: 3)").unwrap_or(usize::MAX);
    let p2_idx = stdout.find("FF FF FF FF (Count: 2)").unwrap_or(usize::MAX);
    let p3_idx = stdout.find("00 00 00 00 (Count: 1)").unwrap_or(usize::MAX);

    assert!(p1_idx < p2_idx, "Pattern 1 should appear before Pattern 2");
    assert!(p2_idx < p3_idx, "Pattern 2 should appear before Pattern 3");

    // Clean up the temporary file
    fs::remove_file(&file_path).expect("Failed to remove temp file");
}

#[test]
fn test_ascii_pattern_extraction() {
    let mut temp_file = NamedTempFile::new().expect("Failed to create temp file");
    let file_path = temp_file.path().to_path_buf();

    let content = b"Hello World!Hello World!Test"; // "Hello World!" repeats twice
    temp_file.write_all(content).expect("Failed to write to temp file");
    temp_file.flush().expect("Failed to flush temp file");

    let output = Command::new("cargo")
        .arg("run")
        .arg("--quiet")
        .arg("--")
        .arg("-f")
        .arg(&file_path)
        .arg("-p")
        .arg("12") // Pattern length "Hello World!" (12 bytes)
        .arg("-t")
        .arg("1")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(output.status.success(), "Command failed with stdout: {}\nstderr: {}", stdout, stderr);
    assert!(stdout.contains("Pattern: 48 65 6C 6C 6F 20 57 6F 72 6C 64 21 (Count: 2) -> Faint Human Traces: A garbled message from the past: \"Hello World!\""));

    fs::remove_file(&file_path).expect("Failed to remove temp file");
}

#[test]
fn test_file_not_found() {
    let non_existent_file = PathBuf::from("non_existent_file_12345.bin");

    let output = Command::new("cargo")
        .arg("run")
        .arg("--quiet")
        .arg("--")
        .arg("-f")
        .arg(&non_existent_file)
        .output()
        .expect("Failed to execute command");

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(!output.status.success());
    assert!(stderr.contains("Error: File not found"));
}

#[test]
fn test_small_file() {
    let mut temp_file = NamedTempFile::new().expect("Failed to create temp file");
    let file_path = temp_file.path().to_path_buf();

    let content = vec![0x01, 0x02]; // Smaller than default pattern length 4
    temp_file.write_all(&content).expect("Failed to write to temp file");
    temp_file.flush().expect("Failed to flush temp file");

    let output = Command::new("cargo")
        .arg("run")
        .arg("--quiet")
        .arg("--")
        .arg("-f")
        .arg(&file_path)
        .arg("-p")
        .arg("4")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(output.status.success(), "Command failed with stdout: {}\nstderr: {}", stdout, stderr);
    assert!(stdout.contains("File is too small to find patterns of length 4."));
    assert!(!stderr.contains("Error")); // Should not be an error

    fs::remove_file(&file_path).expect("Failed to remove temp file");
}
