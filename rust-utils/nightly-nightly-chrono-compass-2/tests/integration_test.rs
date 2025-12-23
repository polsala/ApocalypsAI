#![allow(unused_imports)] // Allow unused imports for test setup

use std::process::Command;
use std::fs::{self, File};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use tempfile::tempdir;
use filetime::{set_file_mtime, FileTime};

// Mock rationale: We create a temporary directory and files with specific, controlled timestamps
// to simulate a file system state. This allows for deterministic and offline testing of the
// chrono-compass logic without relying on the actual system's file times or external resources.
// The `filetime` crate is used to precisely set these timestamps for testing purposes.

#[test]
fn test_chrono_compass_mtime_anomaly() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    // Create files with normal timestamps (within 1 hour of each other)
    let now = SystemTime::now();
    let normal_time_1 = now - Duration::from_secs(30 * 60); // 30 mins ago
    let normal_time_2 = now - Duration::from_secs(15 * 60); // 15 mins ago
    let normal_time_3 = now - Duration::from_secs(45 * 60); // 45 mins ago

    let file1_path = path.join("normal_file1.txt");
    File::create(&file1_path)?.write_all(b"content")?;
    set_file_mtime(&file1_path, FileTime::from_system_time(normal_time_1))?;

    let file2_path = path.join("normal_file2.txt");
    File::create(&file2_path)?.write_all(b"content")?;
    set_file_mtime(&file2_path, FileTime::from_system_time(normal_time_2))?;

    let file3_path = path.join("normal_file3.txt");
    File::create(&file3_path)?.write_all(b"content")?;
    set_file_mtime(&file3_path, FileTime::from_system_time(normal_time_3))?;

    // Create an anomalous file (very old)
    let anomalous_time = now - Duration::from_secs(24 * 3600); // 24 hours ago
    let anomalous_file_path = path.join("anomalous_old_file.txt");
    File::create(&anomalous_file_path)?.write_all(b"content")?;
    set_file_mtime(&anomalous_file_path, FileTime::from_system_time(anomalous_time))?;

    // Create another anomalous file (very new, relative to 'now' used for normal files)
    let future_time = now + Duration::from_secs(2 * 3600); // 2 hours in future
    let anomalous_new_file_path = path.join("anomalous_new_file.txt");
    File::create(&anomalous_new_file_path)?.write_all(b"content")?;
    set_file_mtime(&anomalous_new_file_path, FileTime::from_system_time(future_time))?;

    // Run the chrono-compass command
    let output = Command::new(env!("CARGO_BIN_EXE_chrono-compass"))
        .arg(path.to_str().unwrap())
        .arg("--threshold")
        .arg("3600") // 1 hour threshold
        .arg("--mode")
        .arg("mtime")
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains(&format!("File: {}", anomalous_file_path.display())));
    // The exact drift value depends on 'now', so we check for the magnitude and sign
    assert!(stdout.contains("Chronal Drift:") && stdout.contains("-86400 seconds")); // 24 hours = 86400 seconds
    assert!(stdout.contains(&format!("File: {}", anomalous_new_file_path.display())));
    assert!(stdout.contains("Chronal Drift:") && stdout.contains("7200 seconds")); // 2 hours = 7200 seconds

    // Ensure normal files are NOT flagged
    assert!(!stdout.contains(&format!("File: {}", file1_path.display())));
    assert!(!stdout.contains(&format!("File: {}", file2_path.display())));
    assert!(!stdout.contains(&format!("File: {}", file3_path.display())));

    Ok(())
}

#[test]
fn test_chrono_compass_no_anomaly_within_threshold() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let now = SystemTime::now();
    let time_a = now - Duration::from_secs(10 * 60); // 10 mins ago
    let time_b = now - Duration::from_secs(20 * 60); // 20 mins ago
    let time_c = now - Duration::from_secs(30 * 60); // 30 mins ago

    let file_a_path = path.join("file_a.txt");
    File::create(&file_a_path)?.write_all(b"content")?;
    set_file_mtime(&file_a_path, FileTime::from_system_time(time_a))?;

    let file_b_path = path.join("file_b.txt");
    File::create(&file_b_path)?.write_all(b"content")?;
    set_file_mtime(&file_b_path, FileTime::from_system_time(time_b))?;

    let file_c_path = path.join("file_c.txt");
    File::create(&file_c_path)?.write_all(b"content")?;
    set_file_mtime(&file_c_path, FileTime::from_system_time(time_c))?;

    // Run with a threshold larger than any deviation (e.g., 1 hour = 3600s)
    let output = Command::new(env!("CARGO_BIN_EXE_chrono-compass"))
        .arg(path.to_str().unwrap())
        .arg("--threshold")
        .arg("3600")
        .arg("--mode")
        .arg("mtime")
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);

    assert!(output.status.success());
    assert!(!stdout.contains("[Temporal Resonance Detected]"));

    Ok(())
}

#[test]
fn test_chrono_compass_empty_directory() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();

    let output = Command::new(env!("CARGO_BIN_EXE_chrono-compass"))
        .arg(path.to_str().unwrap())
        .output()?;

    let stdout = String::from_utf8_lossy(&output.stdout);

    assert!(output.status.success());
    assert!(!stdout.contains("[Temporal Resonance Detected]"));
    // Expect no output for an empty directory, or at least no anomalies

    Ok(())
}

#[test]
fn test_chrono_compass_non_existent_path() -> Result<(), Box<dyn std::error::Error>> {
    let non_existent_path = PathBuf::from("non_existent_dir_12345");

    let output = Command::new(env!("CARGO_BIN_EXE_chrono-compass"))
        .arg(non_existent_path.to_str().unwrap())
        .output()?;

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(!output.status.success()); // Should fail because path doesn't exist
    assert!(stderr.contains("Error: Provided path is not a directory."));

    Ok(())
}

#[test]
fn test_chrono_compass_file_as_path() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let file_path = dir.path().join("single_file.txt");
    File::create(&file_path)?.write_all(b"content")?;

    let output = Command::new(env!("CARGO_BIN_EXE_chrono-compass"))
        .arg(file_path.to_str().unwrap())
        .output()?;

    let stderr = String::from_utf8_lossy(&output.stderr);

    assert!(!output.status.success()); // Should fail because path is a file, not a directory
    assert!(stderr.contains("Error: Provided path is not a directory."));

    Ok(())
}
