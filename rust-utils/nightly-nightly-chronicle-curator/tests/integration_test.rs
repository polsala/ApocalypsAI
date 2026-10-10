use std::process::Command;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{SystemTime, Duration};
use chrono::{Utc, TimeZone};

// Helper to create a temporary directory for tests
fn setup_test_env(test_name: &str) -> PathBuf {
    let temp_dir = PathBuf::from(format!("./target/test_temp/{}", test_name));
    if temp_dir.exists() {
        fs::remove_dir_all(&temp_dir).expect("Failed to clean up old test dir");
    }
    fs::create_dir_all(&temp_dir).expect("Failed to create test dir");
    temp_dir
}

// Helper to create a dummy file with a specific modification time
fn create_dummy_file(dir: &Path, filename: &str, mod_time: SystemTime) -> PathBuf {
    let file_path = dir.join(filename);
    fs::write(&file_path, "test content").expect("Failed to write dummy file");
    // Set modification time (creation time is harder to control cross-platform)
    // On Linux, creation time is often not available or is the same as modification time.
    // For robust testing, we'll rely on modification time and test the --modified flag.
    // Mock rationale: We are creating real files in a temporary directory and setting their modification times.
    // This simulates real-world file system behavior without external dependencies.
    filetime::set_file_mtime(&file_path, filetime::FileTime::from_system_time(mod_time))
        .expect("Failed to set modification time");
    file_path
}

#[test]
fn test_dry_run_mode() {
    let temp_dir = setup_test_env("test_dry_run_mode");
    let source_dir = temp_dir.join("source");
    let dest_dir = temp_dir.join("destination");
    fs::create_dir(&source_dir).unwrap();

    let now = SystemTime::now();
    create_dummy_file(&source_dir, "file1.txt", now);
    create_dummy_file(&source_dir, "file2.log", now - Duration::from_secs(86400 * 30)); // 30 days ago

    let output = Command::new("cargo")
        .arg("run")
        .arg("--")
        .arg("-s")
        .arg(&source_dir)
        .arg("-d")
        .arg(&dest_dir)
        .arg("--dry-run")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Dry Run: Would move"));
    assert!(!dest_dir.exists(), "Destination directory should not be created in dry run");
    assert!(source_dir.join("file1.txt").exists(), "Source file should not be moved in dry run");
}

#[test]
fn test_basic_organization_by_modified_time() {
    let temp_dir = setup_test_env("test_basic_organization_by_modified_time");
    let source_dir = temp_dir.join("source");
    let dest_dir = temp_dir.join("destination");
    fs::create_dir(&source_dir).unwrap();

    let file1_time = Utc.with_ymd_and_hms(2023, 1, 15, 10, 0, 0).unwrap().into();
    let file2_time = Utc.with_ymd_and_hms(2024, 3, 5, 14, 30, 0).unwrap().into();

    create_dummy_file(&source_dir, "report.pdf", file1_time);
    create_dummy_file(&source_dir, "image.jpg", file2_time);

    let output = Command::new("cargo")
        .arg("run")
        .arg("--")
        .arg("-s")
        .arg(&source_dir)
        .arg("-d")
        .arg(&dest_dir)
        .arg("--modified") // Explicitly use modified time for consistency
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Curated:"));
    assert!(dest_dir.exists());

    let expected_path1 = dest_dir.join("2023").join("01").join("15").join("report.pdf");
    let expected_path2 = dest_dir.join("2024").join("03").join("05").join("image.jpg");

    assert!(expected_path1.exists(), "File report.pdf not found at expected path");
    assert!(expected_path2.exists(), "File image.jpg not found at expected path");
    assert!(!source_dir.join("report.pdf").exists(), "Original report.pdf should be moved");
    assert!(!source_dir.join("image.jpg").exists(), "Original image.jpg should be moved");
}

#[test]
fn test_handling_non_existent_source() {
    let temp_dir = setup_test_env("test_handling_non_existent_source");
    let non_existent_source = temp_dir.join("non_existent_source");
    let dest_dir = temp_dir.join("destination");

    let output = Command::new("cargo")
        .arg("run")
        .arg("--")
        .arg("-s")
        .arg(&non_existent_source)
        .arg("-d")
        .arg(&dest_dir)
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(!output.status.success()); // Should fail
    assert!(stderr.contains("Error: Source directory"));
}

#[test]
fn test_skipping_hidden_files_by_default() {
    let temp_dir = setup_test_env("test_skipping_hidden_files_by_default");
    let source_dir = temp_dir.join("source");
    let dest_dir = temp_dir.join("destination");
    fs::create_dir(&source_dir).unwrap();

    let now = SystemTime::now();
    create_dummy_file(&source_dir, "visible.txt", now);
    create_dummy_file(&source_dir, ".hidden_file.txt", now);
    fs::create_dir(source_dir.join(".hidden_dir")).unwrap();
    create_dummy_file(&source_dir.join(".hidden_dir"), "inside_hidden.txt", now);

    let output = Command::new("cargo")
        .arg("run")
        .arg("--")
        .arg("-s")
        .arg(&source_dir)
        .arg("-d")
        .arg(&dest_dir)
        .arg("--modified")
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Curated:"));
    assert!(stdout.contains("Files processed: 1")); // Only visible.txt
    assert!(stdout.contains("Directories/files skipped: 2")); // .hidden_file.txt and .hidden_dir

    let today_path = Utc::now().format("%Y/%m/%d").to_string();
    let expected_visible_path = dest_dir.join(&today_path).join("visible.txt");
    let expected_hidden_file_path = dest_dir.join(&today_path).join(".hidden_file.txt");

    assert!(expected_visible_path.exists());
    assert!(!expected_hidden_file_path.exists()); // Should not be moved
    assert!(source_dir.join(".hidden_file.txt").exists()); // Should still be in source
}

#[test]
fn test_including_hidden_files_with_all_flag() {
    let temp_dir = setup_test_env("test_including_hidden_files_with_all_flag");
    let source_dir = temp_dir.join("source");
    let dest_dir = temp_dir.join("destination");
    fs::create_dir(&source_dir).unwrap();

    let now = SystemTime::now();
    create_dummy_file(&source_dir, "visible.txt", now);
    create_dummy_file(&source_dir, ".hidden_file.txt", now);
    fs::create_dir(source_dir.join(".hidden_dir")).unwrap();
    create_dummy_file(&source_dir.join(".hidden_dir"), "inside_hidden.txt", now);

    let output = Command::new("cargo")
        .arg("run")
        .arg("--")
        .arg("-s")
        .arg(&source_dir)
        .arg("-d")
        .arg(&dest_dir)
        .arg("--modified")
        .arg("--all") // Include hidden files
        .output()
        .expect("Failed to execute command");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    println!("STDOUT:\n{}", stdout);
    println!("STDERR:\n{}", stderr);

    assert!(output.status.success());
    assert!(stdout.contains("Curated:"));
    assert!(stdout.contains("Files processed: 2")); // visible.txt and .hidden_file.txt
    assert!(stdout.contains("Directories/files skipped: 1")); // .hidden_dir itself

    let today_path = Utc::now().format("%Y/%m/%d").to_string();
    let expected_visible_path = dest_dir.join(&today_path).join("visible.txt");
    let expected_hidden_file_path = dest_dir.join(&today_path).join(".hidden_file.txt");

    assert!(expected_visible_path.exists());
    assert!(expected_hidden_file_path.exists()); // Should be moved
    assert!(!source_dir.join(".hidden_file.txt").exists()); // Original should be moved
}
